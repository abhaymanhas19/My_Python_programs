from agents import Agent,Runner
import os
os.environ["OPENAI_API_KEY"] = ""
import asyncio

english_agent = Agent(name="English Agent",instructions="You only speak English")
hindi_agent = Agent(name="Hindi Agent",instructions="You only speak Hindi")


triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[hindi_agent, english_agent],
)

async def main():
    result = await Runner.run_sync(triage_agent, input="hello how are you")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())