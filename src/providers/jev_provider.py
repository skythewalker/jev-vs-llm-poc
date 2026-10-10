import time

import httpx

from src.core.config import settings
from src.core.constants import (
    JEV_INPUT_COST_PER_MILLION,
    JEV_OUTPUT_COST_PER_MILLION,
)
from src.core.cost_calculator import calculate_cost
from src.models.schemas import ClassificationResult
from src.providers.base_provider import BaseProvider


class JEVProvider(BaseProvider):
    async def classify(
        self,
        query: str,
    ) -> ClassificationResult:

        start_time = time.perf_counter()

        payload = {
            "model": settings.jev_model,
            "state": query,
            "questions": {
                "intent": {
                    "type": "choice",
                    "instructions": "Classify the user intent",
                    "criteria": {
                        "GREETING": (
                            "Greeting or salutation"
                        ),
                        "INCIDENT_QUERY": (
                            "Looking for incident information"
                        ),
                        "RCA_REQUEST": (
                            "Root cause analysis requests"
                        ),
                        "SUMMARY_REQUEST": (
                            "Requests to summarize alerts, "
                            "incidents, logs, or events"
                        ),
                        "AGENT_ROUTING": (
                            "Requests to select or route "
                            "to an agent"
                        ),
                        "TOOL_SELECTION": (
                            "Requests to choose a tool"
                        ),
                        "SERVICE_IMPACT_ANALYSIS": (
                            "Requests to identify impacted "
                            "applications, dependencies, "
                            "or services"
                        ),
                        "UNKNOWN": (
                            "Does not belong to "
                            "any category"
                        ),
                    },
                }
            },
        }

        try:
            async with httpx.AsyncClient(
                timeout=30
            ) as client:

                response = await client.post(
                    "https://api.typesafe.ai/v1/systemone",
                    headers={
                        "Authorization": (
                            f"Bearer {settings.jev_api_key}"
                        ),
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )

                response.raise_for_status()

                result = response.json()

        except Exception:
            latency_ms = (
                time.perf_counter() - start_time
            ) * 1000

            return ClassificationResult(
                provider="jev",
                intent="UNKNOWN",
                confidence=0.0,
                latency_ms=round(latency_ms, 2),
            )

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        intent_answer = result["answers"]["intent"]

        usage = result.get("usage", {})

        input_tokens = usage.get(
            "input_tokens",
            0,
        )

        output_tokens = usage.get(
            "output_tokens",
            0,
        )

        estimated_cost = calculate_cost(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            input_price_per_million=(
                JEV_INPUT_COST_PER_MILLION
            ),
            output_price_per_million=(
                JEV_OUTPUT_COST_PER_MILLION
            ),
        )

        return ClassificationResult(
            provider="jev",
            intent=intent_answer["choice"],
            confidence=float(
                intent_answer.get(
                    "confidence",
                    0.0,
                )
            ),
            latency_ms=round(
                latency_ms,
                2,
            ),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=estimated_cost,
        )