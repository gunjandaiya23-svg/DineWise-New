# Preferences and current boundaries

The app has one query input. Users express preferences in natural language, for example “quiet Italian restaurants in Tucson under $$”. There is no saved profile, feedback store or preference-learning model.

Rule-based extraction recognizes city, cuisine, price, minimum rating, supported attributes, dietary terms and intent. Exact catalogue fields drive hard filters. Textual preferences that have no implemented filter must not be described as guaranteed constraints.

Dietary terms are currently collected by extraction but are not hard filters. Mentions in review evidence are not medical safety guarantees. The former sidebar profile controls and unused workflow profile state have been removed.

Future preference work should first define how explicit query constraints interact with defaults, then add tests for conflicting requests and missing fields. Persisted profiles and like/dislike ranking bonuses remain outside the current implementation.

## How to phrase a request today

Include each preference in the question itself: “quiet Italian restaurants in Tucson under $$.” The app displays previous turns but does not send them to the next search, so “same city as before” is not a reliable instruction. Exact supported fields, such as city and maximum price bucket, are filtered against the catalogue. “Cozy” can influence word/vector matching but should not be described as a guaranteed attribute unless the parser maps it to an implemented field.

A query can contain conflicting terms or categories the catalogue lacks. The rule parser does not perform human-level clarification. Users should inspect the evidence panel and rephrase a request when the result misses a preference. The four `$` levels are relative dataset categories; they are not currency ranges. No personal profile is saved between sessions.

[Documentation index](README.md)
