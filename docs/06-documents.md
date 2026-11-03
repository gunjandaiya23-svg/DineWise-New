# Evidence profiles

`make docs` builds `data/docs/restaurant_profiles.txt` from processed restaurants
and selected review evidence. Each restaurant has a separate marked block with
its business ID, structured fields, summaries, and review excerpts.

Chunking preserves restaurant boundaries. The profile manifest records the file
checksum and number of restaurants. PDF and DOCX exports are no longer generated.
