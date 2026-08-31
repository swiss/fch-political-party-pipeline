# Party Atlas in RDF

This repository contains all the necessary code to convert the CSV Party Atlas from the University of Bern into RDF format using https://version.link schema.

## Architecture

### Generic Overview

- The University of Bern provides the Party Atlas as a set of CSV files.
- In this repository, a Docker container is created that contains all the necessary code.
- Running the Docker container will convert the CSV files 
  - on the one hand into RDF, that is uploaded to LINDAS
  - on the other hand uploads it to I14Y

## Understanding the RAW CSV files

### party.csv

- This is the main file.
- Each line represents a *vl:Identity* of a party.
- In the field `party_name_id` are some versions of the same party with different names.

## To Remember

- What about the different identifiers from `party_code_id`. In the CSV, these are only given for the *identity* but we should not have information on the *identity* that is not present in a *version* --> current solution, only add identifiers to the vl:Identity to not make it complicated.
- Tried a complete new approach: Only one version per identity. The version has got all the history, the identity only the currently valid data. This aproach is tried in `1_convert_b.ipynb`. --> The problem is, that this approach makes it difficult to build vl:successor and vl:predecessor relationships, because the vl:successor can be the same party (if a split happens, the new party is one follower, but the existing party is also a follower, because it is still existing). So we need to have a vl:successor and vl:predecessor relationship for each version, not only for the identity. So we need to have multiple versions per identity.

## Questions to the University of Bern

- Why use for all dates the same time `12:00:00`? Would it not be better to use only dates and then schema:validFrom 2001-01-01 and schema:validThrough 2001-12-31?
- What is happening, if on the same day, a new party is forming from the split-ofs of two other parties?

## Possible Data Errors

- Party ID 248 "Grütliverein", was associated with SP from 1901 to 1916 (according to HLS). However, in the CSV it is listed as associated with SP from 1901 to 1906.
- Relation ID 126 / Name ID 137: to_date should probably be 2021-01-01 instead of 2020-12-31.
- Party ID 65: Missing name for dates after 1980-01-01.
- Party ID 51: Dissolution in 1999-01-01 but has successor (ID 50) in 2003-05-05
- https://politics.ld.admin.ch/party-version/123_1979-07-01: empty space in front of the name

## Good Examples

- For different child-of relationships: Party 49

## To Do

- create function for pandas lookup in other tables, e.g. for party_name_id, party_code_id, etc.
- create function to convert dictionary keys into RDF predicates and classes, e.g. for party_name_id, party_code_id, etc.

## Unsolved Errors

- Party 158: Has a version 2019-10-08 that should not exist. --> Problem is 158 has dissolution 1990-07-01 but has a successor (Party 159) in 2019-10-08. Same problem for 194 (only one day in between, so probably data error) and probably some others.
  