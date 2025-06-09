# #type:ignore
# import os
# from dotenv import load_dotenv
# from typing import cast
# import chainlit as cl
# from agents import AsyncOpenAI, Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
# import requests

# load_dotenv()
# set_tracing_disabled(True)

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY environment variable is not set")

# client = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# @function_tool
# def get_github_profile(username: str) -> str:
#     pro_response = requests.get(f"https://api.github.com/users/{username}")
#     repos_response = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100")
#     if pro_response.status_code == 200 and repos_response.status_code == 200:
#         profile = pro_response.json()
#         repos = repos_response.json()
#         profile_info = (
#             f"Name: {profile.get('name', 'N/A')}\n"
#             f"Bio: {profile.get('bio', 'N/A')}\n"
#             f"Followers: {profile.get('followers', 0)}\n"
#             f"Following: {profile.get('following', 0)}\n"
#             f"Public Repositories: {profile.get('public_repos', 0)}\n"
#         )
#         repo_info = ""
#         if repos:
#             repo_info = "Repositories:\n" + "\n".join([f"- {repo['name']} ({repo['html_url']})" for repo in repos])
#         else:
#             repo_info = "Repositories: None"
#         return f"{profile_info}{repo_info}"
#     else:
#         return f"Error: Unable to fetch data for username '{username}' from GitHub API"



# agent : Agent = Agent(
#         name="Github profile viewer",
#         instructions="You are a GitHub profile viewer. Your sole purpose is to provide information about a user's GitHub profile when they provide their GitHub username. Call the get_github_profile function with the provided username to fetch and display their name, bio, followers, following, public repositories, and a list of all repository names with their links. If the user provides anything other than a GitHub username or asks unrelated questions, respond with: 'Please provide a valid GitHub username to view profile information.' Do not engage with any other topics or questions.",
#         model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
#         tools=[get_github_profile],
#     )
# @cl.on_chat_start
# async def on_chat_start():
#     cl.user_session.set("chat_history", [])
#     await cl.Message(content="Hello! I'm a Github profile viewer Agent. What's your Github username?").send()

# @cl.on_message
# async def on_message(message: cl.Message):
#     msg = cl.Message(content="Thinking...")
#     await msg.send()
    
#     history = cl.user_session.get("chat_history") or []
#     history.append({"role": "user", "content": message.content})
#     try:
#         response = await Runner.run(agent, history)
#         final_res = response.final_output
        
#         msg.content = final_res
#         await msg.update()
        
#         cl.user_session.set("chat_history", response.to_input_list())
#     except Exception as e:
#         msg.content = f"Error: {e}"
#         await msg.update()

import os
import webbrowser
from dotenv import load_dotenv
import chainlit as cl
from agents import AsyncOpenAI, Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import requests

load_dotenv()
set_tracing_disabled(True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

client = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

@function_tool
def get_github_profile(username: str) -> str:
    pro_response = requests.get(f"https://api.github.com/users/{username}")
    repos_response = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100")
    if pro_response.status_code == 200 and repos_response.status_code == 200:
        profile = pro_response.json()
        repos = repos_response.json()
        # Store repos in user session for later use
        cl.user_session.set("repos", {repo['name'].lower(): repo['html_url'] for repo in repos})
        profile_info = (
            f"Name: {profile.get('name', 'N/A')}\n"
            f"Bio: {profile.get('bio', 'N/A')}\n"
            f"Followers: {profile.get('followers', 0)}\n"
            f"Following: {profile.get('following', 0)}\n"
            f"Public Repositories: {profile.get('public_repos', 0)}\n"
        )
        repo_info = ""
        if repos:
            repo_info = "Repositories:\n" + "\n".join([f"- {repo['name']}" for repo in repos])
        else:
            repo_info = "Repositories: None"
        return f"{profile_info}{repo_info}\n\nWhich repository would you like to visit?"
    else:
        return f"Error: Unable to fetch data for username '{username}' from GitHub API"

@function_tool
def open_repository(repo_name: str) -> str:
    repos = cl.user_session.get("repos", {})
    repo_name_lower = repo_name.lower()
    if repo_name_lower in repos:
        webbrowser.open(repos[repo_name_lower])
        return f"Opening repository '{repo_name}' in your browser."
    else:
        return f"Error: Repository '{repo_name}' not found."

agent : Agent = Agent(
    name="Github Profile Viewer",
    instructions="You are a specialized GitHub profile assistant. Your only role is to assist users with GitHub profile and repository information. When a user provides a GitHub username, call get_github_profile to display their name, bio, followers, following, public repositories, and a list of repository names, then prompt them to select a repository to visit. If the user says 'I want to visit [repository name]', 'open [repository name]', or similar, extract the repository name and call open_repository to open its URL in the browser. For any other input or unrelated questions, respond with: 'Please provide a valid GitHub username or specify a repository to visit (e.g., I want to visit [repo name]). Do not respond to non-GitHub-related topics.",
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash"),
    tools=[get_github_profile, open_repository],
)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])
    cl.user_session.set("repos", {})
    await cl.Message(content="Hello! I'm a GitHub Profile Viewer Agent. Please provide your GitHub username.").send()

@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="Processing...")
    await msg.send()
    
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})
    try:
        response = await Runner.run(agent, history)
        final_res = response.final_output
        
        
        
        msg.content = final_res
        await msg.update()
        
        cl.user_session.set("chat_history", response.to_input_list())
    except Exception as e:
        msg.content = f"Error: {e}"
        await msg.update()