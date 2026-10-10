import asyncio

from openai import AsyncOpenAI

from src.core.config import settings


async def main():
    client = AsyncOpenAI(
        api_key=settings.openai_api_key
    )

    response = await client.responses.create(
        model=settings.gpt_model,
        input="Say hello sky in one sentence"
    )

    print(response.output_text)


asyncio.run(main())