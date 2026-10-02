# HCM_1000 V2


An audited vehicle routing dataset with time windows (VRPTW) for Ho Chi Minh City.


## Download


Download **HCM_1000_V2_Publication_Package.zip** from [Releases](../../releases). Extract the archive before running validation.


## Contents


- 56 instances, each containing 1 depot and 1,000 customers.
- 8 directed road distance/time matrices (1,001 × 1,001), with explicit node-order mappings.
- Independent feasibility witnesses and validation reports for all 56 instances.
- Coordinates, geographic data, routing provenance, construction parameters and documentation.


Feasible witnesses establish feasibility; they are not certified optimal solutions. The package does not include the complete solver-comparison experiment pipeline. Historical map images and notes with incomplete rights information are excluded.


## Validate


Python 3, standard library only. In the extracted `HCM_1000_V2` directory:


```bash
python code/verify_release.py --root .
```


The verifier checks checksums, instance/matrix consistency, route coverage, capacity and time windows. See the packaged data dictionary and provenance for units and assumptions.


## Licences and attribution


See [LICENSING.md](LICENSING.md) for exact scope:


- Database: ODbL 1.0.
- Python code: MIT.
- Newly authored documentation: CC BY 4.0.


OpenStreetMap-derived components require attribution to © OpenStreetMap contributors. See [NOTICE.md](NOTICE.md). Component licences do not replace upstream rights.


## Citation


Le, Tan Long (2026). *HCM_1000 V2: An Audited VRPTW Dataset with Directed Road Costs in Ho Chi Minh City* (Version 2.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.23106441

DOI: [10.5281/zenodo.23106441](https://doi.org/10.5281/zenodo.23106441). Archived dataset: [Zenodo](https://zenodo.org/records/23106441). Use this version-specific DOI when citing the dataset.

