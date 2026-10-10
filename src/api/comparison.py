from fastapi import APIRouter

from src.models.schemas import (
    CompareRequest,
    CompareResponse,
)
from src.services.comparison_service import (
    ComparisonService,
)

router = APIRouter(
    prefix="/compare",
    tags=["comparison"],
)

service = ComparisonService()


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