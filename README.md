# Party Atlas in RDF

This repository contains all the necessary code to convert the CSV Party Atlas from the University of Bern into RDF format using https://version.link schema.

## Understanding the RAW CSV files

### party.csv

- This ist the main file.
- Working hypothesis: Each line represents an *identity* of a party.
- In the field `party_name_id` are some versions of the same party with different names.
- How to determine the number of versions per row in party.csv: Working hypothesis: for each `party_name_id` a version, for each `relationship_id_1` a version and for each `relationship_id_2` a version if it is on the same hierarchical level (country or canton). For all these event, there should be a date extractable.
- Is it enough to use only each line individually or are there cases where we need to combine multiple lines to get a complete picture of a party's identity?
- What about the different identifiers from `party_code_id`. In the CSV, these are only given for the *identity* but we should not have information on the *identity* that is not present in a *version*.
- At the moment, if it is a succession, there is also an entry in the `chronology` generated for the party that is not the successor but ended.

## Questions to the University of Bern

- Why use for all dates the same time `12:00:00`? Would it not be better to use only dates and then schema:validFrom 2001-01-01 and schema:validThrough 2001-12-31?
- What is the difference between `relationship_id_1` and `relationship_id_2`? Is it just a matter of hierarchy (country vs canton) or is there more to it?

## Possible Data Errors

- ID 248 "Grütliverein", was associated with SP from 1901 to 1916 (according to HLS). However, in the CSV it is listed as associated with SP from 1901 to 1906.

## Scratchpad

- We do not work with events because the raw data does not easily allow to determine the events. Idea: use vl:successor <new_version> and ex:splitTo <new_version> to indicate not only the successor but also the process which took place. Is this easy enough to query? No, it is not easy!
