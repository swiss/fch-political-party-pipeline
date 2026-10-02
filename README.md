# Political Party Pipeline

This repository contains all the necessary code to convert the **CSV Party Atlas** from the project [Année Politique Suisse](https://anneepolitique.swiss) from the [University of Bern](https://www.unibe.ch) for two different outlets:

- a [LINDAS](https://ld.admin.ch) *Shared Dimension* in RDF format using the [version.link](https://version.link) schema
- an [I14Y](https://i14y.admin.ch) *Concept*

## Methodology

The conversion is done by using Jupyter notebooks in the folder `notebooks`. The code is intentionally quite verbose and not optimized for performance, as the main goal is to have a clear and understandable code that can be easily modified and extended.

- `1_json.ipynb` converts the multipleCSV files from the University of Bern into a single JSON file that resembles the version.link schema.
- `2a_I14Y.ipynb` contains all the necessary code to convert the JSON file from `1_json.ipynb` into an I14Y concept and upload it to the I14Y platform. It also contains the logic to decide whether a new version of the concept needs to be pushed to the I14Y platform or not.
- `2b_LINDAS.ipynb` contains all the necessary code to convert the JSON file from `1_json.ipynb` into a LINDAS Shared Dimension in RDF according to the version.link schema and upload it to the LINDAS platform.
- `3_queries.ipynb` contains some example queries to work with the LINDAS data.
- `4_delete.ipynb` contains the code to delete the LINDAS Shared Dimension and the I14Y concept from the respective platforms.

## Good Examples

- For different child-of relationships: Party 49