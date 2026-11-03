"""Prompt construction for grounded generation."""

from __future__ import annotations

from typing import Any

import pandas as pd

SYSTEM_PROMPT = """You are DineWise, a restaurant recommendation assistant.

You answer only from the RESTAURANT RECORDS supplied in this prompt. You do
not have access to the internet, live availability, current prices, or
reservations.

Rules:
1. Never invent a restaurant, address, rating, price, dish, dietary fact, or amenity.
2. Ratings and prices come from a static dataset. Describe them as dataset values,
   never as live facts.
3. Never claim that a restaurant is currently open, has a table available, or
   offers a reservation.
4. Every factual sentence must be supported by the supplied records, and must
   mention the restaurant name in **bold**.
5. Never print internal markers such as [RESTAURANT ...], business IDs, or
   parenthesised IDs. Use the human-readable restaurant name only.
6. Never print a bare price bucket ("$", "$$") or a bare number ("4.5") on its
   own. Always explain it: e.g. "Price: $ — Budget-friendly (dataset bucket 1 of 4)"
   and "Rating: 4.5 out of 5 stars (dataset value)".
7. If the records do not contain enough evidence, say so explicitly.
8. Prefer fewer, well-supported recommendations over more, weakly supported ones.
9. Keep the answer under 180 words. Use a short numbered list."""

PRICE_LABELS = {
    1: "Budget-friendly",
    2: "Moderate",
    3: "Higher-priced",
    4: "Most expensive",
}


def _price_text(record: dict[str, Any]) -> str:
    value = record.get("price_range")
    try:
        bucket = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return "price unknown"
    if bucket not in PRICE_LABELS:
        return "price unknown"
    return f"{'$' * bucket} — {PRICE_LABELS[bucket]} (dataset bucket {bucket} of 4)"


def _rating_text(record: dict[str, Any]) -> str:
    value = record.get("stars")
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "rating unknown"
    return f"{value} out of 5 stars (dataset value)"


def _value(record: dict[str, Any], key: str, default: str = "unknown") -> str:
    value = record.get(key)
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return default
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value)


def build_context(hits: list[dict[str, Any]], max_restaurants: int = 5) -> str:
    """Format unique restaurants and their best chunk into a context block."""
    blocks: list[str] = []
    seen: set[str] = set()

    for index, hit in enumerate(hits, start=1):
        record = hit["chunk"]
        business_id = str(record["business_id"])
        if business_id in seen:
            continue
        seen.add(business_id)

        block = [
            f"Record {index}: {_value(record, 'restaurant_name')}",
            f"Business ID (internal only, never print): {business_id}",
            f"City: {_value(record, 'city')}, {_value(record, 'state')}",
            f"Cuisine: {_value(record, 'cuisine_primary')}",
            f"Price: {_price_text(record)}",
            f"Rating: {_rating_text(record)}",
            "Record excerpt:",
            str(record["text"]),
        ]
        blocks.append("\n".join(block))
        if len(blocks) >= max_restaurants:
            break

    return "\n\n".join(blocks) if blocks else "No restaurant records were retrieved."


def build_messages(query: str, hits: list[dict[str, Any]]) -> list[dict[str, str]]:
    context = build_context(hits)
    user = f"""USER QUESTION:
{query}

RESTAURANT RECORDS:
{context}

TASK:
Recommend up to 3 restaurants from the records above as a short numbered list.
For each one, write one connected paragraph (not a terse "name, $, 4.5" line):
**Name** — cuisine and city, then "Price: <dollar signs> — <Budget-friendly/Moderate/Higher-priced/Most expensive> (dataset bucket N of 4)", then
"Rating: <stars> out of 5 stars (dataset value)", then 1-2 sentences explaining
why it matches the request, grounded in the record excerpt. Example:
"1. **Capri Pizza-N-More** — Italian in Tampa. Price: $ — Budget-friendly
(dataset bucket 1 of 4). Rating: 4.5 out of 5 stars (dataset value). Highly
praised for fresh ingredients and generous pizza portions."
If price or rating is missing, write "price unknown" / "rating unknown".
Never output [RESTAURANT ...] tags, business IDs, or bare values like "$, 4.5".
Avoid repeated headings and nested bullet lists. Finish every recommendation
before ending. State once that ratings and prices are dataset values. If the
records do not support an answer, say so.
"""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]
