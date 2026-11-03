# Preferences and current boundaries

The app has one query input. Users express preferences in natural language, for example “quiet Italian restaurants in Tucson under $$”. There is no saved profile, feedback store or preference-learning model.

Rule-based extraction recognizes city, cuisine, price, minimum rating, supported attributes, dietary terms and intent. Exact catalogue fields drive hard filters. Textual preferences that have no implemented filter must not be described as guaranteed constraints.

Dietary terms are currently collected by extraction but are not hard filters. Mentions in review evidence are not medical safety guarantees. The former sidebar profile controls and unused workflow profile state have been removed.

Future preference work should first define how explicit query constraints interact with defaults, then add tests for conflicting requests and missing fields. Persisted profiles and like/dislike ranking bonuses remain outside the current implementation.

[Documentation index](README.md)
