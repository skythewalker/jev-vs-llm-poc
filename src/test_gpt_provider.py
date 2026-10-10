import asyncio

from src.providers.gpt_provider import GPTProvider


async def main():
    provider = GPTProvider()

    result = await provider.classify(
        "Show all open incidents"
    )

    print(result.model_dump())


asyncio.run(main())