# What the workflow returns

The generated answer is a Markdown string, not a JSON object. The prompt asks for names and excludes business IDs from the visible answer. The workflow returns a Python dictionary containing that string and internal diagnostics.

| Key | Meaning |
|---|---|
| `query` | Original user text |
| `constraints` | Parsed Constraints dataclass |
| `hits` | Retrieved records as score/chunk dictionaries |
| `answer` | Recommendation or fallback text |
| `passed`, `validation` | Answer checks and hard/soft failures |
| `retry_count` | Number of generation retries |
| `out_of_scope`, `refused`, `reason` | Scope and retrieval refusal information |
| `fallback_used` | Whether the final response came from fallback logic |
| `trace` | Step descriptions used in diagnostics |

Not every path populates every field. A scope refusal can happen before constraints or hits exist, so callers should use `.get()` for optional values. The constraints object is not directly JSON serializable without conversion. Streamlit renders the answer, city coverage, a catalogue-backed price/rating summary for named restaurants, and expandable restaurant records and evidence excerpts. It stores returned state in session history but does not send earlier turns into a new query.

[Documentation index](../README.md)

## Example state shape

```python
{
    "query": "Italian restaurants in Tampa under $$",
    "constraints": Constraints(city="Tampa", cuisines=["Italian"], max_price_bucket=2),
    "hits": [{"score": 0.03, "chunk": {"business_id": "example-id", "city": "Tampa"}}],
    "answer": "1. **Example Bistro** — ...",
    "passed": True,
    "retry_count": 0,
}
```

The values above illustrate the structure; they are not a recorded run. In a refusal, `hits` or `validation` may be absent. The app stores the state alongside each assistant message so expanders can show the evidence for that particular turn.
