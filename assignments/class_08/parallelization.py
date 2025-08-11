import asyncio
from agents import Agent, ItemHelpers, Runner
from config import config
from openai.types.responses import ResponseTextDeltaEvent

#assignment 3: parallelization.py

spanish_agent = Agent(
    name="SpanishAgent",
    instructions="You translate the user's message to Spanish.",
)

translation_picker_agent = Agent(
    name="TranslationPickerAgent",
    instructions="You pick the best Spanish translation from the given options.",
)

async def main():
    msg = input("Hi! Enter a message, and we'll translate it to Spanish.\n\n > ")

    res_1, res_2, res_3 = await asyncio.gather(
        Runner.run(
                spanish_agent,
                msg,
                run_config=config,
            ),
        Runner.run(
                spanish_agent,
                msg,
                run_config=config,
            ),
        Runner.run(
                spanish_agent,
                msg,
                run_config=config,
            ),
    )
    outputs = [
            ItemHelpers.text_message_outputs(res_1.new_items),
            ItemHelpers.text_message_outputs(res_2.new_items),
            ItemHelpers.text_message_outputs(res_3.new_items),
        ]
    translations = "\n\n".join(outputs)
    print(f"\n\nTranslations:\n\n{translations}")
    try:
        result = Runner.run_streamed(translation_picker_agent, input=f"Input: {msg}\n\nTranslations:\n{translations}", run_config=config)
        print("\n\nBest translation:\n")
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
                continue
    except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())


