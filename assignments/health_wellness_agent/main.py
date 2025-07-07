# #type: ignore
# import asyncio
# from context import UserSessionContext
# from utils.streamingformain import stream_conversation
# from hooks import HealthPlannerHooks, HealthPlannerRunHooks
# from dotenv import load_dotenv
# from agent import create_health_agent
# from guardrails import InputGuardrailTripwireTriggered
# from guardrails import OutputGuardrailTripwireTriggered

# load_dotenv()

# async def main():
    
#     print("\n🌟 === Health & Wellness Assistant === 🌟")
#     print("🏃‍♂️ Your guide to fitness goals, meal planning, and workouts! 🥗")
#     print("💡 Type 'quit' to exit or 'debug' to toggle debug mode\n")
    
#     debug_mode = True  # Debug mode enabled by default
    
#     try:
#         name = input("👤 What's your name? ")
#         context = UserSessionContext(name=name, uid=1)
        
#         agent = create_health_agent()
#         agent_hooks = HealthPlannerHooks()
#         agent.hooks = agent_hooks
        
#         print(f"\n✅ Agent ready with hooks: {type(agent_hooks).__name__}")
#         print(f"🐛 Debug mode: {'ON' if debug_mode else 'OFF'}")
        
#         runner_hooks = HealthPlannerRunHooks()
        

#         while True:
#             try:
#                 print("\n" + "="*40)
#                 user_input = input(f"👤 {name}: ")
                
#                 if user_input.lower() in ['quit', 'exit', 'bye']:
#                     print("\n👋 Stay healthy! Goodbye!")
#                     break
#                 elif user_input.lower() == 'debug':
#                     debug_mode = not debug_mode
#                     print(f"\n🐛 Debug mode: {'ON' if debug_mode else 'OFF'}")
#                     continue
                    
#                 print("\n🤖 Assistant Response:")
#                 print("-"*40)
                
#                 if debug_mode:
#                     print(f"🔍 Context logs before: {len(context.handoff_logs)} entries")
                
#                 await stream_conversation(agent, user_input, context, runner_hooks)
                
#                 print("\n📜 Log Summary:")
#                 print("-"*40)
#                 if context.handoff_logs:
#                     print(f"📋 Total logs: {len(context.handoff_logs)}")
#                     if debug_mode:
#                         print("🔍 Recent logs (last 5):")
#                         for log in context.handoff_logs[-5:]:
#                             print(f"  📝 {log}")
#                 else:
#                     print("⚠️ No logs generated")
                    
#                 print("="*40 + "\n")
                
#             except KeyboardInterrupt:
#                 print("\n👋 Stay healthy! Goodbye!")
#                 break
#             except Exception as e:
#                 print(f"\n❌ Error in conversation: {str(e)}")
#                 if debug_mode:
#                     import traceback
#                     print("\n🔍 Debug Traceback:")
#                     print("-"*40)
#                     traceback.print_exc()
#                     print("-"*40)
                    
#     except InputGuardrailTripwireTriggered as e:
#         reason = e.guardrail_result.reasoning
#         print(f"❌ Input rejected by guardrail: {reason}")
#     except OutputGuardrailTripwireTriggered as e:
#         reason = e.guardrail_result.reasoning
#         print(f"⚠️ Output blocked by guardrail: {reason}")      
#     except KeyboardInterrupt:
#         print("\n👋 Stay healthy! Goodbye!")
#     except Exception as e:
#         print(f"\n❌ Fatal error: {str(e)}")
#         if debug_mode:
#             import traceback
#             print("\n🔍 Error Traceback:")
#             print("-"*40)
#             traceback.print_exc()
#             print("-"*40)

# if __name__ == "__main__":
#     asyncio.run(main())

# type: ignore
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio
import uuid
from context import UserSessionContext
from agent import create_health_agent
from utils.streamingformain import stream_conversation
from openai.types.responses import ResponseTextDeltaEvent
from guardrails import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from hooks import HealthPlannerRunHooks
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# In-memory stores (simplified for demo, use database in production)
session_store = {}
response_store = {}

# Pydantic model for user input
class UserInput(BaseModel):
    name: str
    user_input: str
    session_id: str = None

@app.get("/")
async def root():
    return {"message": "Health & Wellness Assistant API. Use /api/input (POST) or /api/response/{session_id} (GET)."}

@app.post("/api/input")
async def process_input(user_input: UserInput, api_key: str):
    """Process user input and return agent response"""
    if api_key != "secret":
        return {"error": "Invalid API Key"}
    
    try:
        # Generate or use session ID
        session_id = user_input.session_id or str(uuid.uuid4())
        
        # Initialize or retrieve context
        if session_id not in session_store:
            context = UserSessionContext(name=user_input.name, uid=len(session_store) + 1)
            session_store[session_id] = context
        else:
            context = session_store[session_id]
        
        # Create agent
        agent = create_health_agent()
        runner_hooks = HealthPlannerRunHooks()
        
        # Collect response by awaiting stream_conversation
        response = []
        result = await stream_conversation(agent, user_input.user_input, context, runner_hooks)
        async for event in result.stream_events():  # Assuming stream_conversation returns an object with stream_events
            if event.type == "raw_response_event":
                if hasattr(event.data, 'delta') and event.data.delta:
                    response.append(event.data.delta)
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    response.append(f"\n🔧 Using {event.item.raw_item.name}...")
                elif event.item.type == "tool_call_output_item":
                    response.append(" Done.")
            elif event.type == "agent_updated_stream_event":
                response.append(f"\n🤝 Handing off to {event.data.name}...")
            elif event.type == "text_delta_event":
                response.append(event.delta)
        
        # Store response
        response_store[session_id] = response
        
        return {"response": "".join(response), "session_id": session_id}
    except InputGuardrailTripwireTriggered as e:
        raise HTTPException(status_code=400, detail=f"Input rejected: {e.guardrail_result.reasoning}")
    except OutputGuardrailTripwireTriggered as e:
        raise HTTPException(status_code=400, detail=f"Output blocked: {e.guardrail_result.reasoning}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/response/{session_id}")
async def get_response(session_id: str, api_key: str):
    """Retrieve stored response for a session"""
    if api_key != "secret":
        return {"error": "Invalid API Key"}
    
    if session_id not in response_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"response": "".join(response_store[session_id]), "session_id": session_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


