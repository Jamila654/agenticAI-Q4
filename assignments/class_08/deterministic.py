import asyncio
from pydantic import BaseModel
from agents import Agent, Runner
from config import config
from openai.types.responses import ResponseTextDeltaEvent

#assignment 1: deterministic.py

story_outline_agent = Agent(
    name="StoryOutlineAgent",
    instructions="Generate a very short story outline based on the user's input.",
)

class OutlineChecker(BaseModel):
    good_quality: bool
    is_scifi: bool

outline_checker_agent = Agent(
    name="OutlineCheckerAgent",
    instructions="Read the given story outline, and judge the quality. Also, determine if it is a scifi story.",
    output_type=OutlineChecker
)

story_agent = Agent(    
    name="StoryAgent",
    instructions="Generate a story based on the given outline.",
    output_type=str
)

async def main():
    user_input = input("What kind of story do you want?\n > ")

    outline_result = await Runner.run(
        starting_agent=story_outline_agent,
        input=user_input,
        run_config=config
    )

    print("Outline Generated")

    outline_check_result = await Runner.run(
        starting_agent=outline_checker_agent,
        input=outline_result.final_output,
        run_config=config
    )

    print("Outline Checked")

    assert isinstance(outline_check_result.final_output, OutlineChecker)
    if not outline_check_result.final_output.good_quality:
        print("Outline is not good quality, so we stop here.")
        exit(0)

    if not outline_check_result.final_output.is_scifi:
            print("Outline is not a scifi story, so we stop here.")
            exit(0)

    print("Outline is good quality and a scifi story, so we continue to write the story.")
    
    try:
            result = Runner.run_streamed(story_agent, input=outline_result.final_output, run_config=config)
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print("Story Generated 👇\n\n")
                    print(event.data.delta, end="", flush=True)
                    continue
    except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())