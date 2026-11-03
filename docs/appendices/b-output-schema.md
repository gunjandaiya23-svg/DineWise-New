# What the workflow returns

The generated answer is a Markdown string, not a JSON object. The workflow returns a Python dictionary containing that string and internal diagnostics.

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

Not every path populates every field. A scope refusal can happen before constraints or hits exist, so callers should use `.get()` for optional values. The constraints object is not directly JSON serializable without conversion. Streamlit renders the answer, city coverage and expandable restaurant records and evidence excerpts.

[Documentation index](../README.md)
