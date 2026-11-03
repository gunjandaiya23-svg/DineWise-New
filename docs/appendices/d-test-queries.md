# Fixed evaluation queries

These queries come from `src/dinewise/eval/__init__.py`. Twelve are intended to be answerable; three test refusal behavior. Passing this small suite does not establish general accuracy.

| ID | Facet | Query |
|---|---|---|
| Q01 | cuisine | Find Italian restaurants with good reviews in Philadelphia. |
| Q02 | budget | Recommend restaurants under $$ in Philadelphia. |
| Q03 | review_aspect | Which restaurants have the best food quality according to reviews? |
| Q04 | ambience | Find restaurants with positive ambience reviews in Philadelphia. |
| Q05 | personalization | Recommend a restaurant for a family dinner in Philadelphia. |
| Q06 | comparison | Compare two Italian restaurants in Philadelphia based on reviews. |
| Q07 | dessert | Which restaurants in New Orleans are praised for their desserts? |
| Q08 | dietary | Find restaurants with vegetarian options in Philadelphia. |
| Q09 | cuisine | Find pizza restaurants in Indianapolis. |
| Q10 | cuisine | Find seafood restaurants in Tampa. |
| Q11 | ranking | Which restaurant in Tucson offers the best value for money? |
| Q12 | multi_constraint | Family-friendly Mexican restaurant in Philadelphia under $$. |
| Q13 | out_of_scope | Give me the live availability of Reading Terminal Market tonight. |
| Q14 | out_of_scope | Recommend a restaurant in Las Vegas. |
| Q15 | unsupported | Which restaurant in Philadelphia has a rooftop pool? |
