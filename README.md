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
- Party ID 51: Dissolution in 1999-01-01 but has successor (ID 50) in 2003-05-05

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

## Currently Wrong

- Child Of Relationships: https://politics.ld.admin.ch/party-version/59_1987-07-01 is a child of https://politics.ld.admin.ch/party-version/43_1983-06-15 but this version ends on 1987-07-01 so it should not be a child of this version --> others are probably affected as well. Reason is probably a wrong <= comparison of the dates. We need to check this and fix it. --> fixed
- If there are e.g. only two versions with different names and also the last hast a valid_through date, then the last version is created as still existing, e.g. Party ID 43 (the error is in line 157 of 1_convert.ipynb).

## Good Examples

- For different child-of relationships: Party 49

## Uuups

What is happening, if on the same day, a new party is forming from the split-ofs of two other parties?

## 04.08.26

- a split ends one version and starts two versions.
- a accessed ends two versions and starts one version.

Probably it is easier to create two events for a split (for the party that existed before and after the split), and the split that is ending the version, should somehow be connected to all the events that started this version --> every information that is needed to create a new version should be available right at the beginning of the version, otherwise there are complex operations needed. So this should be done already on the event creation

## 07.08.26

Complete new approach: Only one version per identity. The version has got all the history, the identity only the currently valid data. This aproach is tried in `1_convert_b.ipynb`. --> The problem is, that this approach makes it difficult to build vl:successor and vl:predecessor relationships, because the vl:successor can be the same party (if a split happens, the new party is one follower, but the existing party is also a follower, because it is still existing). So we need to have a vl:successor and vl:predecessor relationship for each version, not only for the identity. So we need to have multiple versions per identity.

## 10.08.26

Steps:

- get all the dates that are relevant
- check whether last date creates a new version (then version history is open ended) or only ends the last version (then version history is closed)
- then versions are known and can be created --> then we have dates and versions
- check all the events for all dates and see if they have an opening effect on the new version or closing effects on the version before

Example: Party 1 is founded in 1900-01-01, has a name change in 1950-01-01 and 2000-01-01, Party 2 splits from Party 1

View Party 1:

- relevant dates: 1900-01-01, 1950-01-01, 2000-01-01
- 2001-01-01 creates a new version because after the split, party 1 still exists, so the version history is open ended. So we have three versions for Party 1: 1900-01-01, 1950-01-01 and 2000-01-01
- Events:
  - 1900-01-01 founding, starting event for version 1900-01-01
  - 1950-01-01 name change, stop event for version 1900-01-01, starting event for version 1950-01-01
  - 2000-01-01 split, stop event for version 1950-01-01, starting event for version 2000-01-01

View Party 2:

- relevant dates: 2000-01-01
- 2000-01-01 creates a new version because it is the founding of Party 2, so the version history is open ended. So we have one version for Party 2: 2000-01-01
- Events:
  - 2000-01-01 founding, starting event for version 2000-01-01

Questions for each party:

- what are the relevant dates for this party?
- what are the versions for this party?

And then for each version in the party:

- what are the starting events for this version?
- what is the currently valid name for this version? (can only be one, otherwise it is an error)
- what are the currently valid relationships for this version? (can be multiple at the same time)
- what are the stopping events for this version?
- what are the successors of this version? (can be multiple at the same time; predecessors to a version are not relevant here, this backwards-link will only be made in the RDFization)

Events are instantaneous, e.g name-change, split, founding, dissolution, etc. Relationships are valid for a certain time period, e.g. child-of, observer-in, affiliated-with, etc.

All Events:

- founding
  - starts always a new version
  - stops never the previous version
- dissolution
  - starts never a new version
  - stops always the previous version
- name-change-start
  - starts always a new version
  - stops never the previous version
- name-change-stop
  - starts never a new version
  - stops always the previous version
- relationship-start (e.g. child-of, observer-in, affiliated-with)
  - starts always a new version
  - stops never the previous version
- relationship-stop
  - starts never a new version
  - stops always a previous version

- split for the before existing party
  - starts always a new version
  - stops always the previous version
- split for the new party
  - starts always a new version
  - stops never the previous version
- accessed for the party that gets accessed
  - starts always a new version
  - stops always the previous version
- accessed for the party that accesses
  - starts always a new version
  - stops always the previous version
- successor for the party that gets succeeded
  - starts never a new version
  - stops always the previous version
- successor for the party that succeeds
  - starts always a new version
  - stops never the previous version
  