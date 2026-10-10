from src.models.schemas import CompareRequest


request = CompareRequest(
    query="Show all open incidents"
)

print(request.model_dump())