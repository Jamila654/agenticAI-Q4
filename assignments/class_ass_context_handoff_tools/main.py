#type: ignore
import asyncio
from stream import stream_main


print("Welcome!\n")
user_name = input("What is your name? ")
user_query = input("What is your question? ")
print("\n")
async def run_stream(name: str = user_name, query: str = user_query):
    async for data in stream_main(name, query):
        print(data, flush=True)  # Process each yielded value

if __name__ == "__main__":
    asyncio.run(run_stream())