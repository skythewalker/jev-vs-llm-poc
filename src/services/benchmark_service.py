import json
from pathlib import Path

from src.core.config import settings
from src.services.comparison_service import (
    ComparisonService,
)


class BenchmarkService:
    def __init__(self) -> None:
        self.comparison_service = (
            ComparisonService()
        )

    async def run_benchmark(self) -> dict:

        dataset = json.loads(
            Path(
                "testdata/intents.json"
            ).read_text(
                encoding="utf-8"
            )
        )

        total_queries = len(dataset)

        jev_correct = 0
        gpt_correct = 0

        jev_total_latency = 0.0
        gpt_total_latency = 0.0

        jev_total_input_tokens = 0
        jev_total_output_tokens = 0

        gpt_total_input_tokens = 0
        gpt_total_output_tokens = 0

        jev_total_cost = 0.0
        gpt_total_cost = 0.0

        results = []

        for item in dataset:

            query = item["query"]
            expected = item["expected"]

            comparison = (
                await self.comparison_service
                .compare(query)
            )

            if comparison.jev.intent == expected:
                jev_correct += 1

            if comparison.gpt.intent == expected:
                gpt_correct += 1

            jev_total_latency += (
                comparison.jev.latency_ms
            )

            gpt_total_latency += (
                comparison.gpt.latency_ms
            )

            jev_total_input_tokens += (
                comparison.jev.input_tokens
            )

            jev_total_output_tokens += (
                comparison.jev.output_tokens
            )

            gpt_total_input_tokens += (
                comparison.gpt.input_tokens
            )

            gpt_total_output_tokens += (
                comparison.gpt.output_tokens
            )

            jev_total_cost += (
                comparison.jev.estimated_cost
            )

            gpt_total_cost += (
                comparison.gpt.estimated_cost
            )

            results.append(
                {
                    "query": query,
                    "expected": expected,
                    "jev_intent":
                        comparison.jev.intent,
                    "gpt_intent":
                        comparison.gpt.intent,
                    "jev_correct":
                        comparison.jev.intent
                        == expected,
                    "gpt_correct":
                        comparison.gpt.intent
                        == expected,
                }
            )

        if (
            jev_total_cost > 0
            and gpt_total_cost > 0
        ):

            if gpt_total_cost > jev_total_cost:

                cost_ratio = round(
                    gpt_total_cost
                    / jev_total_cost,
                    2,
                )

                cost_summary = (
                    f"JEV was {cost_ratio}x cheaper than GPT"
                )

            else:

                cost_ratio = round(
                    jev_total_cost
                    / gpt_total_cost,
                    2,
                )

                cost_summary = (
                    f"GPT was {cost_ratio}x cheaper than JEV"
                )

        else:

            cost_summary = (
                "Cost comparison unavailable"
            )

        summary = {
            "total_queries":
                total_queries,
            "gpt_model":
                settings.gpt_model,
            "jev_model":
                settings.jev_model,
            "jev": {
                "accuracy_percent":
                    round(
                        (
                            jev_correct
                            / total_queries
                        )
                        * 100,
                        2,
                    ),
                "average_latency_ms":
                    round(
                        jev_total_latency
                        / total_queries,
                        2,
                    ),
                "input_tokens":
                    jev_total_input_tokens,
                "output_tokens":
                    jev_total_output_tokens,
                "total_cost":
                    round(
                        jev_total_cost,
                        8,
                    ),
            },
            "gpt": {
                "accuracy_percent":
                    round(
                        (
                            gpt_correct
                            / total_queries
                        )
                        * 100,
                        2,
                    ),
                "average_latency_ms":
                    round(
                        gpt_total_latency
                        / total_queries,
                        2,
                    ),
                "input_tokens":
                    gpt_total_input_tokens,
                "output_tokens":
                    gpt_total_output_tokens,
                "total_cost":
                    round(
                        gpt_total_cost,
                        8,
                    ),
                 "cost_summary":
                                cost_summary,
            },
        }

        return {
            "summary": summary,
        }