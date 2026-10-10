import asyncio

from src.services.comparison_service import ComparisonService


async def main():
    service = ComparisonService()

    result = await service.compare(
        "Show all open incidents"
    )

    print(result.model_dump())


if __name__ == "__main__":
    asyncio.run(main())