# Artifact for On the Diagnosis of Flaky Job Failures

Replication package of the paper [On the Diagnosis of Flaky Job Failures:
Understanding and Prioritizing Failure Categories](./PAPER.pdf) accepted at the 47th International Conference on Software Engineering ICSE SEIP 2025.

## Purpose

This replication package includes Jupyter Notebooks and full analysis results of the [study](./study/) to provide in-depth details of the analysis and foster replication.

It also includes the [source code](./src/flakeranker/) of the **FlakeRanker** CLI tool. This tool is an engineered version of the notebook scripts to facilitate reuse of our RFM prioritization approach, through automated labeling of flaky job failures with failure categories and prioritization of the categories using RFM modeling.

As such, we claim the following badges:

- `Available`
- `Reusable`

## Data

To conduct the study, we collected build job data from GitLab projects using the **python-gitlab** library. For confidentiality reasons, the data collected from TELUS projects are not included. However, we prepared a build job [dataset](./example/data/) collected from the open-source project _Veloren_ to demonstrate the **FlakeRanker** CLI tool's functionalities.

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

### Content

We list the Jupyter Notebooks used to answer the RQs and included in this repository.

**PQ.** [Data Labeling Process](./study/data_labeling_process/02_failure_categories_labeling.ipynb)

**RQ1-3.** [RFM Analysis](./study/rfm_analysis/03_label_prioritization.ipynb)

- RQ1. What are the main categories of flaky failures?
- RQ2. Which failure categories are the most costly?
- RQ3. How do the failure categories evolve over time?

**RQ4.** [RFM Modeling and Prioritization](./study/rfm_prioritization/04_categories_rfm_prioritization.ipynb)

- RQ4. What are the priority flaky failure categories?

#### Additional Study Materials

The [`study/results/`](./study/results/) directory contains additional research results materials including:

- Full figures of categories evolution and related costs
- Computed RFM values and scores
- Scatter plots of Recency vs Frequency, Frequency vs Monetary, and Recency vs Monetary values
- Correlation matrix of RFM scores used for K-means clustering
- Clustering model dump and clustering results.

## FlakeRanker CLI Tool for Reuse

### ⚙️ Installation

We provide two options for intalling `flakeranker`.

#### 1. Build Docker Image (recommended)

Clone this repository. In the root directory, run the following command.

```sh
docker build --tag flakeranker --file docker/Dockerfile .
```

#### 2. Install Python Package

Install the [**`flakeranker`**](https://pypi.org/project/flakeranker) Python library.

```sh
pip install flakeranker
```

## 🚀 Quickstart Reuse Example

### Unzip the example dataset

```sh
unzip example/data/veloren.zip -d example/data/
```

It outputs inside the `example/data/veloren/` directory, the `jobs.csv` and `labeled_jobs.csv` files.

### Run the experiment on the example dataset

We recommend running the experiment using the already labeled dataset for faster execution. To do so, simply copy and run the following command depending on your installation choice.

To further test the labeling processing on a clean dataset (which might take a while ~ 34min on an Ubuntu 22.04 RAM 16GB Dual Core i7 2.80GHz), simply change `labeled_jobs.csv` with `jobs.csv` in the command.

Using the Docker Image

```sh
docker run \
-v ./example/data/veloren/labeled_jobs.csv:/opt/flakeranker/jobs.csv \
-v ./example/results/:/opt/flakeranker/ \
flakeranker run /opt/flakeranker/jobs.csv -o /opt/flakeranker/
```

Using the Python Package

```sh
flakeranker run ./example/data/veloren/labeled_jobs.csv -o ./example/results/
```

**FlakeRanker CLI** outputs the experiments results into the [example/results/](example/results/) directory as follows:

- `labeled_jobs.csv`: Labeled dataset of jobs produced by the labeler module.
- `rfm_dataset.csv`: RFM dataset of flaky job failure categories produced by the analyzer module.
- `ranked_rfm_dataset.csv`: Ranked RFM dataset including the scores, cluster, and pattern produced by the ranker module. Outlier categories are affected to the cluster -1.

For more details on each FlakeRanker sub-command, please read the [documentation](./example/README.md) also available on the [official page](https://pypi.org/project/flakeranker/) of the flakeranker python package.

## Citation

```bibtex
@inproceedings{aidasso_diagnosis_2025,
  Author = {Aïdasso, Henri and Bordeleau, Francis and Tizghadam, Ali},
  Title = {On the {Diagnosis} of {Flaky} {Job} {Failures}: {Understanding} and {Prioritizing} {Failure} {Categories}},
  Year = {2025},
  Booktitle = {Proceedings of 2025 {IEEE}/{ACM} 47th {International} {Conference} on {Software} {Engineering} ({ICSE})},
  Pages = {To appear}
}
```
