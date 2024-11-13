# Understanding and Prioritizing Flaky Failures at TELUS

This repository contains the replication package of identifying flaky failure categories and using RFM analysis to prioritize them.

## Requirements

* [Python](https://www.python.org/downloads/) >= 3.10
* [Poetry](https://python-poetry.org/)

## Getting started

Install dependencies

```script
poetry install
```

Create (or activate) virtual environment

```script
poetry shell
```

## Study

In the following, we reference Jupyter Notebooks present in this repository, that we used to answer the RQs.

PQ. [Data Labeling Process](./src/02_failure_categories_labeling.ipynb)

__Final Failure Categories Regexes [patterns_refined.csv](./src/scripts/patterns_refined.csv)__

RQ1-3. [Flaky Failure Categories RFM Analysis](./src/03_label_prioritization.ipynb)

* RQ1. What are the main categories of flaky failures?
* RQ2. Which failure categories are the most costly?
* RQ3. How do the failure categories evolve over time?
* [Addition RFM Analysis results](./src/04_labels_rfm_analysis.ipynb)

[RQ4. What are the priority flaky failure categories?](./src/04_labels_rfm_clustering.ipynb)

Additionnal results materials can be found in the [`src/results`](./src/results/) directory. It includes full figures, computed RFM values, and clustering model and analysis results.
