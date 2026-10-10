from fastapi import FastAPI

from src.api.comparison import router as comparison_router

app = FastAPI(
    title="JEV vs GPT Comparison POC",
    version="1.0.0",
)

app.include_router(
    comparison_router
)


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }