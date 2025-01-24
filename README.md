# Artifact for On the Diagnosis of Flaky Job Failures

Replication package of the paper [On the Diagnosis of Flaky Job Failures:
Understanding and Prioritizing Failure Categories](./PAPER.pdf) accepted at the 47th International Conference on Software Engineering ICSE SEIP 2025.

## Purpose

This replication package includes Jupyter Notebooks and full analysis results of the [study](./study/) to provide in-depth details of the analysis and foster replication. It also includes [flakeranker](./src/flakeranker/), an engineered version of the notebooks in a CLI tool to facilitate reuse of our approach for identifying and prioritizing flaky job failure categories based on RFM measures.

As such, we claim the following badges:

- `Available`
- `Reusable`

## Data

To conduct the study, we collected build job data from GitLab projects using the [python-gitlab](https://python-gitlab.readthedocs.io/en/stable/) package. For confidentiality reasons, the data collected from TELUS projects are not included. However, we prepared a [build job dataset](./example/data/) collected from the open-source project [Veloren](https://gitlab.com/veloren/veloren) to demonstrate the **FlakeRanker** CLI tool's functionalities.

## Available Study Replication Package

### Requirements

- [Python](https://www.python.org/downloads/) >= 3.10
- [Poetry](https://python-poetry.org/)

### Getting started

Install dependencies

```script
poetry install
```

Create (or activate) virtual environment

```script
poetry shell
```

In the following, we reference Jupyter Notebooks present in this repository, that we used to answer the RQs.

**PQ.** [Data Labeling Process](./study/data_labeling_process/02_failure_categories_labeling.ipynb)

**RQ1-3.** [RFM Analysis](./study/rfm_analysis/03_label_prioritization.ipynb)

- RQ1. What are the main categories of flaky failures?
- RQ2. Which failure categories are the most costly?
- RQ3. How do the failure categories evolve over time?

**RQ4.** [RFM Modeling and Prioritization](./study/rfm_prioritization/04_categories_rfm_prioritization.ipynb)

- RQ4. What are the priority flaky failure categories?

### Additional Materials

The [`study/results/`](./study/results/) directory contains additional research results materials including:

- Full figures of categories evolution and related costs
- Computed RFM values and scores
- Scatter plots of Recency vs Frequency, Frequency vs Monetary, and Recency vs Monetary values
- Correlation matrix of RFM scores used for K-means clustering
- Clustering model dump and clustering results.

## FlakeRanker CLI Tool for Reuse

### Installation

We offer two approaches for `flakeranker` installation. We recommend building the Docker image.

#### Docker Image Build

```sh
docker build --tag flakeranker --file docker/Dockerfile .
```

#### Python Package

Install the **`flakeranker`** Python library.

```sh
pip install flakeranker
```

## Quickstart Reuse Example

**Unzip the prepared dataset.** It outputs the `example/data/jobs.csv` and `example/data/labeled_jobs.csv` file.

```sh
unzip ./example/data/jobs.zip
```

**Run the experiment on the example dataset.**

Using the Docker Image

```sh
docker run \
-v ./example/data/labeled_jobs.csv:/opt/flakeranker/jobs.csv \
-v ./example/results/:/opt/flakeranker/ \
flakeranker run /opt/flakeranker/jobs.csv -o /opt/flakeranker/
```

Using the Python Package

```sh
flakeranker run ./example/data/labeled_jobs.csv -o ./example/results/
```

**FlakeRanker** outputs the experiments results into the [example/results/](example/results/) directory, including:

- `labeled_jobs.csv`: Labeled dataset of jobs produced by the labeler module.
- `rmf_dataset.csv`: RFM dataset of flaky job failure categories produced by the analyzer module.
- `ranked_rfm_dataset.csv`: Ranked RFM dataset including the cluster and RFM patterns produced by the ranker module. Outlier categories are affected to the cluster -1.

For more details on each FlakeRanker sub-command, please read the [documentation](./example/README.md) in the example folder.
