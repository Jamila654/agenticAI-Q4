OpenRouter AI Agent

A simple Python script to create a command-line AI agent using OpenRouter's DeepSeek model via the OpenAI SDK and openai-agents package.
Purpose
This script enables users to interact with an AI agent powered by OpenRouter's DeepSeek model (deepseek/deepseek-v3:free). The agent responds to user input in English through a command-line interface.
Requirements

Python 3.11+
Dependencies (listed in pyproject.toml):
openai>=1.0.0
openai-agents>=0.0.16
python-dotenv>=1.1.0




Get your API key from OpenRouter.


Usage
Run the script using uv:
uv run python main.py


Enter a query (e.g., "What's your name?").
Type exit to quit.
The agent responds in English using OpenRouter’s DeepSeek model.

Code Overview

Libraries: Uses asyncio for asynchronous API calls, openai for OpenRouter’s API, agents for agent orchestration, and python-dotenv for environment variables.
Functionality: Initializes an AsyncOpenAI client with OpenRouter’s endpoint, creates a deepseek agent, and processes user input in a loop.
Tracing: Disables logging with set_tracing_disabled(True) to reduce overhead.

Limitations

No Chat History: The agent doesn’t retain conversation context between inputs.
Model Name: Verify deepseek/deepseek-v3:free on OpenRouter’s model list.
Rate Limits: OpenRouter’s free models are limited to 200 requests/day and 20 requests/minute.
