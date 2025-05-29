#type: ignore
import os
from dotenv import load_dotenv
import chainlit as cl
from litellm import completion
import json
from typing import Optional, Dict


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
github_client_id = os.getenv("OAUTH_GITHUB_CLIENT_ID")
github_client_secret = os.getenv("OAUTH_GITHUB_CLIENT_SECRET")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

@cl.oauth_callback
def oauth_callback(
  provider_id: str,
  token: str,
  raw_user_data: Dict[str, str],
  default_user: cl.User,
) -> Optional[cl.User]:
  return default_user

@cl.on_chat_start
async def start():
    cl.user_session.set("chat_history", [])
    await cl.Message(content="Hello! I'm a chatbot powered by Gemini. How can I help you?").send()

@cl.on_message
async def main(message: cl.Message): 
    history = cl.user_session.get("chat_history", [])
    history.append({"role": "user", "content": message.content})
    
    try:
        response = completion(
            model="gemini/gemini-2.0-flash",
            api_key=GEMINI_API_KEY,
            messages=history,
        )
        final_response: str = response.choices[0].message.content
        await cl.Message(content=final_response).send()
        
        history.append({"role": "assistant", "content": final_response})
    
        cl.user_session.set("chat_history", history)
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        await cl.Message(content=error_message).send()
        history.append({"role": "assistant", "content": error_message})
        cl.user_session.set("chat_history", history)

@cl.on_chat_end
def end():
    history = cl.user_session.get("chat_history")
    with open("chat_history.json", "w") as f:
        json.dump(history, f, indent=2)
    print("Chat history saved.")