import asyncio

from src.providers.jev_provider import JEVProvider


async def main():
    provider = JEVProvider()

    result = await provider.classify(
        "Hello"
    )

    print(result.model_dump())


asyncio.run(main())