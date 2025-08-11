from __future__ import annotations
import asyncio
from dataclasses import dataclass
from typing import Literal
from agents import Agent, ItemHelpers, Runner, TResponseInputItem
from config import config

#assisgnment 2: llm_as_judge.py

story_outline_generator = Agent(
    name="StoryOutlineGenerator",
    instructions=(
        "You generate a very short story outline based on the user's input. "
        "If there is any feedback provided, use it to improve the outline."
    ),
)

@dataclass
class EvaluationFeedback:
    feedback: str
    score: Literal["pass", "needs_improvement", "fail"]

evaluator = Agent(
    name="Evaluator",
    instructions=(
        "You evaluate a story outline and decide if it's good enough. "
        "If it's not good enough, you provide feedback on what needs to be improved. "
        "Never give it a pass on the first try. After 5 attempts, you can give it a pass if the story outline is good enough - do not go for perfection"
    ),
    output_type=EvaluationFeedback
)

async def main():
    msg = input("What kind of story would you like to hear?\n > ")

    input_items: list[TResponseInputItem] = [{"content": msg, "role": "user"}]

    latest_outline: str | None = None

    while True:
        story_outline_result = await Runner.run(
                story_outline_generator,
                input_items,
                run_config=config,
            )
        input_items = story_outline_result.to_input_list()
        latest_outline = ItemHelpers.text_message_outputs(story_outline_result.new_items)
        print("Story outline generated\n")

        evaluator_result = await Runner.run(evaluator, input_items, run_config=config)
        result: EvaluationFeedback = evaluator_result.final_output

        print(f"Evaluator score: {result.score}\n")

        if result.score == "pass":
                print("Story outline is good enough, exiting.\n")
                break

        print("Re-running with feedback\n")

        input_items.append({"content": f"Feedback: {result.feedback}", "role": "user"})

    print(f"Final story outline: {latest_outline}")

if __name__ == "__main__":
    asyncio.run(main())

