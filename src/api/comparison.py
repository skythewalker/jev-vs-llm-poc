from fastapi import APIRouter

from src.models.schemas import (
    CompareRequest,
    CompareResponse,
)
from src.services.comparison_service import (
    ComparisonService,
)
from src.services.benchmark_service import (
    BenchmarkService,
)


router = APIRouter(
    prefix="/compare",
    tags=["comparison"],
)

service = ComparisonService()
benchmark_service = (
    BenchmarkService()
)


@router.post(
    "",
    response_model=CompareResponse,
)
async def compare(
    request: CompareRequest,
) -> CompareResponse:
    """
    Compare JEV and GPT for a given query.
    """

    return await service.compare(
        request.query
    )

@router.post("/benchmark")
async def benchmark():

    return await benchmark_service.run_benchmark()