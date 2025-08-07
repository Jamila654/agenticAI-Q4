from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from agents import Agent, Runner, SQLiteSession
from openai.types.responses import ResponseTextDeltaEvent
import json
import os
from config import config

app = FastAPI(
    title="Personal Study Buddy API",
    description="A simple FastAPI for Personal Study Buddy with session management.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://study-buddy-theta-six.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent
agent = Agent(
    name="StudyBuddy",
    instructions="You are a Personal Study Buddy. Help users study a chosen topic by asking relevant questions, evaluating their answers, and providing feedback. Use the conversation history to tailor questions and avoid repetition. Be encouraging, concise, and educational.",
)

# Database and sessions file paths
db_path = "session.db"
sessions_file = "sessions.json"

# Load known sessions from file
def load_sessions():
    if os.path.exists(sessions_file):
        with open(sessions_file, 'r') as f:
            return json.load(f)
    return []
known_sessions = load_sessions()
session_counter = max(int(sid.split('_')[-1]) for sid in known_sessions if sid.startswith("study_session_")) if known_sessions else 0

def save_sessions():
    with open(sessions_file, 'w') as f:
        json.dump(known_sessions, f)

@app.get("/")
async def root():
    return {"message": "Welcome to the Personal Study Buddy API. Use /sessions, /new_session, /clear_session, or /chat."}

@app.get("/sessions")
async def list_sessions():
    return {"sessions": known_sessions}

@app.post("/new_session")
async def new_session():
    global session_counter
    session_counter += 1
    session_id = f"study_session_{session_counter}"
    known_sessions.append(session_id)
    save_sessions()
    return {"session_id": session_id, "message": f"Created new session: {session_id}"}

@app.post("/clear_session")
async def clear_session(session_id: str):
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id parameter is required")
    if session_id not in known_sessions:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    session = SQLiteSession(session_id=session_id, db_path=db_path)
    await session.clear_session()
    known_sessions.remove(session_id)
    save_sessions()
    return {"session_id": session_id, "message": f"Cleared session: {session_id}"}

async def stream_chat(session_id: str, text: str):
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id parameter is required")
    if session_id not in known_sessions:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    if not text.strip():
        raise HTTPException(status_code=400, detail="text parameter cannot be empty")
    
    try:
        session = SQLiteSession(session_id=session_id, db_path=db_path)
        result = Runner.run_streamed(agent, input=text, session=session, run_config=config)
        
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                if event.data.delta:
                    chunk = json.dumps({"chunk": event.data.delta})
                    yield f"data: {chunk}\n\n"
            elif event.type == "agent_updated_stream_event":
                chunk = json.dumps({"agent_updated": event.new_agent.name})
                yield f"data: {chunk}\n\n"
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    chunk = json.dumps({"tool_called": event.item.raw_item.name})
                    yield f"data: {chunk}\n\n"
                elif event.item.type == "tool_call_output_item":
                    chunk = json.dumps({"tool_output": event.item.output})
                    yield f"data: {chunk}\n\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")

@app.post("/chat")
async def chat_stream(session_id: str, text: str):
    return StreamingResponse(
        stream_chat(session_id, text),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)