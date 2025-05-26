# #type: ignore
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import requests
import os


load_dotenv()


set_tracing_disabled(disabled=True)

MODEL = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

@function_tool
def get_weather(city: str):
    """
    Get the current weather for a given city.
    """
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        raise ValueError("WEATHER_API_KEY is not set in the environment variables.")
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "main" not in data:
            return f"Could not get weather for {city}. Please check the city name."

        weather_desc = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        return f"The weather in {city} is {weather_desc}, temperature is {temperature}°C, feels like {feels_like}°C."

    except Exception as e:
        return f"Error fetching weather: {str(e)}"


agent = Agent(
    name="Weather Agent",
    instructions="You are a weather agent. You will answer questions about the weather. if its not a related question, you will answer it with 'I am sorry, I can only answer questions about the weather.\n",
    model=LitellmModel(
        model=MODEL,
        api_key=GEMINI_API_KEY,
    ),
    tools=[get_weather]
)
print("=============== WEATHER AGENT ===============\n Asking the agent to answer a question about the weather.\n Type 'exit' to stop the agent.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Exiting the agent.")
        break
    result = Runner.run_sync(agent, user_input)
    print(result.final_output)
    




