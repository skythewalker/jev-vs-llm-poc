import asyncio
import csv
import json
from datetime import datetime
from pathlib import Path

from src.services.comparison_service import ComparisonService


async def main() -> None:
    dataset = json.loads(
        Path("testdata/intents.json").read_text(
            encoding="utf-8"
        )
    )

    service = ComparisonService()

    total_queries = len(dataset)

    benchmark_rows = []

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

    print("\nStarting benchmark...\n")

    for index, item in enumerate(dataset, start=1):
        query = item["query"]
        expected = item["expected"]

        result = await service.compare(query)

        benchmark_rows.append(
            {
                "query": query,
                "expected_intent": expected,

                "jev_intent": result.jev.intent,
                "jev_confidence": result.jev.confidence,
                "jev_latency_ms": result.jev.latency_ms,
                "jev_input_tokens": result.jev.input_tokens,
                "jev_output_tokens": result.jev.output_tokens,
                "jev_cost": result.jev.estimated_cost,
                "jev_correct": (
                    result.jev.intent == expected
                ),

                "gpt_intent": result.gpt.intent,
                "gpt_confidence": result.gpt.confidence,
                "gpt_latency_ms": result.gpt.latency_ms,
                "gpt_input_tokens": result.gpt.input_tokens,
                "gpt_output_tokens": result.gpt.output_tokens,
                "gpt_cost": result.gpt.estimated_cost,
                "gpt_correct": (
                    result.gpt.intent == expected
                ),

                "latency_winner": (
                    "JEV"
                    if result.jev.latency_ms
                    < result.gpt.latency_ms
                    else "GPT"
                ),

                "confidence_winner": (
                    "JEV"
                    if result.jev.confidence
                    > result.gpt.confidence
                    else "GPT"
                ),
            }
        )

        print("\n" + "=" * 80)
        print(f"Test Case #{index}")
        print("=" * 80)

        print(f"Query              : {query}")
        print(f"Expected Intent    : {expected}")

        print(
            f"JEV Intent         : "
            f"{result.jev.intent}"
        )
        print(
            f"JEV Confidence     : "
            f"{result.jev.confidence}"
        )
        print(
            f"JEV Latency (ms)   : "
            f"{result.jev.latency_ms}"
        )
        print(
            f"JEV Input Tokens   : "
            f"{result.jev.input_tokens}"
        )
        print(
            f"JEV Output Tokens  : "
            f"{result.jev.output_tokens}"
        )
        print(
            f"JEV Cost ($)       : "
            f"{result.jev.estimated_cost:.8f}"
        )

        print()

        print(
            f"GPT Intent         : "
            f"{result.gpt.intent}"
        )
        print(
            f"GPT Confidence     : "
            f"{result.gpt.confidence}"
        )
        print(
            f"GPT Latency (ms)   : "
            f"{result.gpt.latency_ms}"
        )
        print(
            f"GPT Input Tokens   : "
            f"{result.gpt.input_tokens}"
        )
        print(
            f"GPT Output Tokens  : "
            f"{result.gpt.output_tokens}"
        )
        print(
            f"GPT Cost ($)       : "
            f"{result.gpt.estimated_cost:.8f}"
        )

        if result.jev.intent == expected:
            jev_correct += 1

        if result.gpt.intent == expected:
            gpt_correct += 1

        jev_total_latency += result.jev.latency_ms
        gpt_total_latency += result.gpt.latency_ms

        jev_total_input_tokens += (
            result.jev.input_tokens
        )
        jev_total_output_tokens += (
            result.jev.output_tokens
        )

        gpt_total_input_tokens += (
            result.gpt.input_tokens
        )
        gpt_total_output_tokens += (
            result.gpt.output_tokens
        )

        jev_total_cost += (
            result.jev.estimated_cost
        )
        gpt_total_cost += (
            result.gpt.estimated_cost
        )

    jev_accuracy = (
        (jev_correct / total_queries) * 100
        if total_queries
        else 0
    )

    gpt_accuracy = (
        (gpt_correct / total_queries) * 100
        if total_queries
        else 0
    )

    jev_avg_latency = (
        jev_total_latency / total_queries
        if total_queries
        else 0
    )

    gpt_avg_latency = (
        gpt_total_latency / total_queries
        if total_queries
        else 0
    )

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_queries": total_queries,
        "jev": {
            "accuracy_percent": round(
                jev_accuracy,
                2,
            ),
            "average_latency_ms": round(
                jev_avg_latency,
                2,
            ),
            "input_tokens": (
                jev_total_input_tokens
            ),
            "output_tokens": (
                jev_total_output_tokens
            ),
            "total_cost": round(
                jev_total_cost,
                8,
            ),
        },
        "gpt": {
            "accuracy_percent": round(
                gpt_accuracy,
                2,
            ),
            "average_latency_ms": round(
                gpt_avg_latency,
                2,
            ),
            "input_tokens": (
                gpt_total_input_tokens
            ),
            "output_tokens": (
                gpt_total_output_tokens
            ),
            "total_cost": round(
                gpt_total_cost,
                8,
            ),
        },
    }

    json_file = "benchmark_results.json"

    Path(json_file).write_text(
        json.dumps(
            report,
            indent=4,
        ),
        encoding="utf-8",
    )

    csv_file = "benchmark_results.csv"

    with open(
        csv_file,
        mode="w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=benchmark_rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(benchmark_rows)

    print(
        f"\nBenchmark results saved to "
        f"{json_file}"
    )

    print(
        f"Benchmark results saved to "
        f"{csv_file}"
    )

    print("\n")
    print("=" * 80)
    print("BENCHMARK REPORT")
    print("=" * 80)

    print("\nJEV RESULTS")
    print("-" * 40)
    print(
        f"Accuracy (%)        : "
        f"{jev_accuracy:.2f}"
    )
    print(
        f"Average Latency (ms): "
        f"{jev_avg_latency:.2f}"
    )
    print(
        f"Input Tokens        : "
        f"{jev_total_input_tokens}"
    )
    print(
        f"Output Tokens       : "
        f"{jev_total_output_tokens}"
    )
    print(
        f"Total Cost ($)      : "
        f"{jev_total_cost:.8f}"
    )

    print("\nGPT RESULTS")
    print("-" * 40)
    print(
        f"Accuracy (%)        : "
        f"{gpt_accuracy:.2f}"
    )
    print(
        f"Average Latency (ms): "
        f"{gpt_avg_latency:.2f}"
    )
    print(
        f"Input Tokens        : "
        f"{gpt_total_input_tokens}"
    )
    print(
        f"Output Tokens       : "
        f"{gpt_total_output_tokens}"
    )
    print(
        f"Total Cost ($)      : "
        f"{gpt_total_cost:.8f}"
    )

    print("\nOVERALL SUMMARY")
    print("-" * 40)
    print(
        f"Total Queries       : "
        f"{total_queries}"
    )

    if jev_avg_latency < gpt_avg_latency:
        print(
            f"Latency Winner      : "
            f"JEV "
            f"({gpt_avg_latency - jev_avg_latency:.2f} ms faster)"
        )
    else:
        print(
            f"Latency Winner      : "
            f"GPT "
            f"({jev_avg_latency - gpt_avg_latency:.2f} ms faster)"
        )

    if jev_accuracy > gpt_accuracy:
        print(
            f"Accuracy Winner     : "
            f"JEV "
            f"({jev_accuracy - gpt_accuracy:.2f}% higher)"
        )
    elif gpt_accuracy > jev_accuracy:
        print(
            f"Accuracy Winner     : "
            f"GPT "
            f"({gpt_accuracy - jev_accuracy:.2f}% higher)"
        )
    else:
        print(
            "Accuracy Winner     : TIE"
        )

    print(
        "\nBenchmark completed successfully."
    )


if __name__ == "__main__":
    asyncio.run(main())