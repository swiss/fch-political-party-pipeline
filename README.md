# Party Atlas in RDF

This repository contains all the necessary code to convert the CSV Party Atlas from the University of Bern into RDF format using https://version.link schema.

## Understanding the RAW CSV files

### party.csv

- This ist the main file.
- Working hypothesis: Each line represents an *identity* of a party.
- In the field `party_name_id` are some versions of the same party with different names.
- How to determine the number of versions per row in party.csv: Working hypothesis: for each `party_name_id` a version, for each `relationship_id_1` a version and for each `relationship_id_2` a version if it is on the same hierarchical level (country or canton). For all these event, there should be a date extractable.

## Questions to the University of Bern

- Why use for all dates the same time `12:00:00`? Would it not be better to use only dates and then schema:validFrom 2001-01-01 and schema:validThrough 2001-12-31?
