import json
import time

from openai import AsyncOpenAI

from src.core.config import settings
from src.core.pricing import (
    OPENAI_PRICING,
    calculate_cost,
)
from src.models.schemas import ClassificationResult
from src.providers.base_provider import BaseProvider


class GPTProvider(BaseProvider):

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key
        )

    async def classify(
        self,
        query: str,
    ) -> ClassificationResult:

        start_time = time.perf_counter()

        response = await self.client.responses.create(
            model=settings.gpt_model,
            input=f"""
You are an intent classifier.

Classify the query into one of:

GREETING
INCIDENT_QUERY
AGENT_ROUTING
RCA_REQUEST
SUMMARY_REQUEST
TOOL_SELECTION
SERVICE_IMPACT_ANALYSIS
UNKNOWN

Return ONLY JSON.

Example:
{{
    "intent": "GREETING",
    "confidence": 0.99
}}

Query:
{query}
"""
        )

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        raw_response = response.output_text
        usage = response.usage

        input_tokens = usage.input_tokens
        output_tokens = usage.output_tokens

        pricing = OPENAI_PRICING[
            settings.gpt_model
        ]

        estimated_cost = calculate_cost(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            input_price=pricing[
                "input_per_million"
            ],
            output_price=pricing[
                "output_per_million"
            ],
        )

        try:
            parsed = json.loads(
                raw_response
            )

            intent = parsed["intent"]
            confidence = parsed["confidence"]

        except Exception:

            intent = "UNKNOWN"
            confidence = 0.0

        return ClassificationResult(
            provider="gpt",
            intent=intent,
            confidence=confidence,
            latency_ms=round(
                latency_ms,
                2,
            ),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=estimated_cost,
        )