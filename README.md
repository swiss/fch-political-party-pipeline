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

- Party ID 248 "Grütliverein", was associated with SP from 1901 to 1916 (according to HLS). However, in the CSV it is listed as associated with SP from 1901 to 1906.
- Relation ID 126 / Name ID 137: to_date should probably be 2021-01-01 instead of 2020-12-31.
- Party ID 65: Missing name for dates after 1980-01-01.

## Relationships

There are two main kinds of relationships between parties:

- shape-changing relationships
- hierarchical relationships

### Shape-Changing Relationships

These relationships change the "shape" of the party in that it creates really a new party. The following relationships are shape-changing:

- successor-of
- split-from
- accessed

Shape-changing relationships have to be considered on both sides of the relationship. For example, if a party is a split-from another party, then both parties have to have a new version. Also the one that exists before the split has to have a new version, because it is not the same party anymore after the split.

### Hierarchical Relationships

These relationships are more "hierarchical" and do not create new versions on the other side of the relationship, because otherwise, it would always create an avalanche of new versions (basically all parties would have to have a new version, if they are connected to a mutual root party). The following relationships are hierarchical:

- child-of
- observer-in
- affiliated-with

Hierarchical relationships have to be only considered of the party that is on the "lower" side of the hierarchy. For example, if a party is a child-of another party, then only the child party has to have a new version, but not the parent party.

## Scratchpad

- We do not work with events because the raw data does not easily allow to determine the events. Idea: use vl:successor <new_version> and ex:splitTo <new_version> to indicate not only the successor but also the process which took place. Is this easy enough to query? No, it is not easy!

## Dates

Dates are always given as "YYYY-MM-DDT12:00:00". Dates are read from the CSV files and converted to date objects. If a date is not given, it is set to None. Beginning Dates are taken as given, ending dates are set to the day before.

## To Do

- Probably, the relations child-of, observer-in, affiliated-with are more "hierarchical" and do not create new versions on the other side of the relationship (e.g. child-of, observer-in, affiliated-with). We need to check this and remove it from the chronology of the other party.

successor-of, split-from, accessed: do not have `to_date`
child-of, observer-in, affiliated-with: can have `to_date`
