# On the Diagnosis of Flaky Job Failures

Replication package of the paper [On the Diagnosis of Flaky Job Failures:
Understanding and Prioritizing Failure Categories](/) accepted at the 47th International Conference on Software Engineering ICSE SEIP 2025.

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

## Study Replication Package

In the following, we reference Jupyter Notebooks and Python scripts present in this repository, that we used to answer the RQs.

__PQ.__ [Data Labeling Process](./src/02_failure_categories_labeling.ipynb)

* Final Failure Categories Regexes __[patterns_refined.csv](./src/scripts/patterns_refined.csv)__

__RQ1-3.__ [Flaky Failure Categories' Analysis of Frequency, Costs, and Evolution](./src/03_label_prioritization.ipynb)

* RQ1. What are the main categories of flaky failures?
* RQ2. Which failure categories are the most costly?
* RQ3. How do the failure categories evolve over time?
* [Complementary RFM Analysis](./src/04_labels_rfm_analysis.ipynb)

__RQ4.__ What are the priority flaky failure categories? [RFM Clustering](./src/04_labels_rfm_clustering.ipynb)

## Additional Materials

The directory [`src/results/`](./src/results/) contains additional research results materials including:

* Full figures of categories evolution and related costs
* Computed RFM values and scores
* Scatter plots of Recency vs Frequency, Frequency vs Monetary, and Recency vs Monetary values
* Correlation matrix of RFM scores used for K-means clustering
* Clustering model dump and clustering results.
