OPENAI_PRICING = {
    "gpt-4.1-mini": {
        "input_per_million": 0.40,
        "output_per_million": 1.60,
    },
    "gpt-5-mini": {
        "input_per_million": 0.25,
        "output_per_million": 2.00,
    },
    "gpt-5.4-mini": {
        "input_per_million": 0.75,
        "output_per_million": 4.50,
    },
}

# TypeSafe JEV pricing
# Based on current public pricing used by the POC.
JEV_PRICING = {
    "jev-latest": {
        "input_per_million": 0.042,
        "output_per_million": 0.0,
    }
}


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    input_price: float,
    output_price: float,
) -> float:
    """
    Calculate cost using per-million-token pricing.
    """

    return round(
        (
            (input_tokens / 1_000_000) * input_price
            + (output_tokens / 1_000_000) * output_price
        ),
        8,
    )