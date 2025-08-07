from agents import Agent, Runner, SQLiteSession
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
from config import config
import json
import os

async def main():
    # Initialize the agent with your instructions
    agent = Agent(
        name="StudyBuddy",
        instructions="You are a Personal Study Buddy. Help users study a chosen topic by asking relevant questions, evaluating their answers, and providing feedback. Use the conversation history to tailor questions and avoid repetition. Be encouraging, concise, and educational.",
    )

    # Database path for session storage
    db_path = "session.db"
    sessions_file = "sessions.json"

    # Load known sessions from file, or initialize empty list
    known_sessions = []
    if os.path.exists(sessions_file):
        with open(sessions_file, 'r') as f:
            known_sessions = json.load(f)
    session_counter = max(int(sid.split('_')[-1]) for sid in known_sessions if sid.startswith("study_session_")) if known_sessions else 0

    def save_sessions():
        with open(sessions_file, 'w') as f:
            json.dump(known_sessions, f)

    # Welcome message
    print("Welcome to Personal Study Buddy!")
    print("Study any topic with interactive quizzes. Sessions are saved in session.db.")
    print("\nCommands:")
    print("  !new - Start a new session")
    print("  !list - List known sessions")
    print("  !switch <session_id> - Switch to another session")
    print("  !clear <session_id> - Clear a session")
    print("  exit - Exit the program")
    print("\nChoose a session or create a new one.")

    # Initialize session
    session_id = "study_session_1"
    session = SQLiteSession(session_id=session_id, db_path=db_path)
    if session_id not in known_sessions:
        known_sessions.append(session_id)
        save_sessions()

    # Session selection
    print("\nKnown sessions:", ", ".join(known_sessions) if known_sessions else "No sessions found.")
    print("Enter a session ID, '!new' for a new session, or press Enter for the default.")
    session_choice = input("Session: ").strip()
    if session_choice == "!new":
        session_counter += 1
        session_id = f"study_session_{session_counter}"
        known_sessions.append(session_id)
        save_sessions()
        session = SQLiteSession(session_id=session_id, db_path=db_path)
        print(f"Started new session: {session_id}")
    elif session_choice in known_sessions:
        session_id = session_choice
        session = SQLiteSession(session_id=session_id, db_path=db_path)
        print(f"Loaded session: {session_id}")
    elif session_choice:
        print(f"Session '{session_choice}' not found. Using default: {session_id}")
    else:
        print(f"Using default session: {session_id}")

    print("\nEnter a topic (e.g., 'Python programming') or answer questions.")

    while True:
        user_input = input("\nUser: ").strip()
        if user_input.lower() == "exit":
            break
        elif user_input == "!new":
            session_counter += 1
            session_id = f"study_session_{session_counter}"
            known_sessions.append(session_id)
            save_sessions()
            session = SQLiteSession(session_id=session_id, db_path=db_path)
            print(f"Started new session: {session_id}")
            continue
        elif user_input == "!list":
            print("Known sessions:", ", ".join(known_sessions) if known_sessions else "No sessions found.")
            continue
        elif user_input.startswith("!switch "):
            new_session_id = user_input[8:].strip()
            if new_session_id in known_sessions:
                session_id = new_session_id
                session = SQLiteSession(session_id=session_id, db_path=db_path)
                print(f"Switched to session: {session_id}")
            else:
                print(f"Session '{new_session_id}' not found.")
            continue
        elif user_input.startswith("!clear "):
            clear_session_id = user_input[7:].strip()
            if clear_session_id in known_sessions:
                clear_session = SQLiteSession(session_id=clear_session_id, db_path=db_path)
                await clear_session.clear_session()
                known_sessions.remove(clear_session_id)
                save_sessions()
                print(f"Cleared session: {clear_session_id}")
                if clear_session_id == session_id:
                    session_id = "study_session_1"
                    session = SQLiteSession(session_id=session_id, db_path=db_path)
                    if session_id not in known_sessions:
                        known_sessions.append(session_id)
                        save_sessions()
                    print(f"Switched to default session: {session_id}")
            else:
                print(f"Session '{clear_session_id}' not found.")
            continue
        try:
            # Stream responses using the Runner, leveraging session for history
            result = Runner.run_streamed(agent, input=user_input, session=session, run_config=config)
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)
                    continue
                elif event.type == "agent_updated_stream_event":
                    print(f"Agent updated: {event.new_agent.name}\n")
                    continue
                elif event.type == "run_item_stream_event":
                    if event.item.type == "tool_call_item":
                        print(f"Tool call: {event.item.raw_item.name}\n")
                    elif event.item.type == "tool_call_output_item":
                        print(f"-- Tool output: {event.item.output}\n")
                    elif event.item.type == "message_output_item":
                        pass
                    else:
                        pass  # Ignore other event types
        except Exception as e:
            print(f"An error occurred: {e}")

    print(f"\nThanks for studying! Progress saved in session.db (Session: {session_id}).")

if __name__ == "__main__":
    asyncio.run(main())