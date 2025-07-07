# type: ignore
import os
import sys
import io
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from dotenv import load_dotenv
from context import UserSessionContext
from agent import create_health_agent
from utils.streamingformain import stream_conversation
from hooks import HealthPlannerHooks, HealthPlannerRunHooks
from guardrails import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from fastapi.middleware.cors import CORSMiddleware

# load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

app = FastAPI(
    title="Health & Wellness Assistant API",
    description="API for a Health & Wellness chatbot assistant with goal analysis, meal planning, workouts, and tracking.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://agentic-ai-q4-lfx4.vercel.app/", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    user_name: str = Field(..., description="User's name")
    message: str = Field(..., description="User's message to the assistant")

class ChatResponse(BaseModel):
    user_id: str
    reply: str
    timestamp: str

# In-memory user session contexts keyed by user_id
user_sessions: dict[str, UserSessionContext] = {}

# Create the health agent once (reuse for all requests)
agent = create_health_agent()
agent.hooks = HealthPlannerHooks()
runner_hooks = HealthPlannerRunHooks()

@app.get("/")
async def root():
    return {"message": "Health & Wellness Assistant API"}

@app.post("/chat/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Retrieve or create user session context
    context = user_sessions.get(request.user_id)
    if context is None:
        context = UserSessionContext(name=request.user_name, uid=hash(request.user_id))
        user_sessions[request.user_id] = context

    # Capture printed output by redirecting stdout
    buffer = io.StringIO()
    loop = asyncio.get_event_loop()

    try:
        # Redirect stdout to buffer
        original_stdout = sys.stdout
        sys.stdout = buffer

        # Run the streaming conversation (which prints output)
        await stream_conversation(
            agent=agent,
            user_input=request.message,
            context=context,
            runner_hooks=runner_hooks
        )

        # Restore stdout
        sys.stdout = original_stdout

        assistant_reply = buffer.getvalue().strip()
        buffer.close()

        if not assistant_reply:
            assistant_reply = "Sorry, I couldn't generate a response. Please try again."

        return ChatResponse(
            user_id=request.user_id,
            reply=assistant_reply,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    except InputGuardrailTripwireTriggered as e:
        sys.stdout = original_stdout
        reason = e.guardrail_result.reasoning
        raise HTTPException(status_code=400, detail=f"Input rejected by guardrail: {reason}")

    except OutputGuardrailTripwireTriggered as e:
        sys.stdout = original_stdout
        reason = e.guardrail_result.reasoning
        raise HTTPException(status_code=500, detail=f"Output blocked by guardrail: {reason}")

    except Exception as e:
        sys.stdout = original_stdout
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)