#type: ignore
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from main_agent import main_agent
from context import UserInfo
from config import config
from agents import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from stream import stream_main
from hooks import DemoRunHooks
import uvicorn
import json

app = FastAPI(
    title="Maths Or Python Chat Agent",
    description="A chat agent that answers questions about maths or python.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "This is a maths or python chat agent."}

async def chat(message: UserInfo):
    if not message.text or not message.text.strip():
        raise HTTPException(status_code=400, detail="Message text cannot be empty")
    
    hooks = DemoRunHooks()
    
    try:
        async for data in stream_main(name=message.name or "User", query=message.text, hooks=hooks):
            yield f"data: {data}\n\n"
    except InputGuardrailTripwireTriggered as e:
        error_msg = json.dumps({"error": f"Input rejected: {e.guardrail_result.output_info.reasoning}"})
        yield f"data: {error_msg}\n\n"
    except OutputGuardrailTripwireTriggered as e:
        error_msg = json.dumps({"error": f"Output blocked: {e.guardrail_result.output_info.reasoning}"})
        yield f"data: {error_msg}\n\n"
    except Exception as e:
        error_msg = json.dumps({"error": f"Agent processing failed: {str(e)}"})
        yield f"data: {error_msg}\n\n"

@app.post("/chat/")
async def chat_stream(message: UserInfo):
    return StreamingResponse(
        chat(message),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)