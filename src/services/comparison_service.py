import asyncio

from src.models.schemas import CompareResponse
from src.providers.gpt_provider import GPTProvider
from src.providers.jev_provider import JEVProvider


class ComparisonService:
    def __init__(self) -> None:
        self.gpt_provider = GPTProvider()
        self.jev_provider = JEVProvider()

    async def compare(
        self,
        query: str,
    ) -> CompareResponse:
        """
        Compare the classification results returned
        by JEV and GPT for the same query.
        """

        jev_result, gpt_result = await asyncio.gather(
            self.jev_provider.classify(query),
            self.gpt_provider.classify(query),
        )

        return CompareResponse(
            query=query,
            jev=jev_result,
            gpt=gpt_result,
        )