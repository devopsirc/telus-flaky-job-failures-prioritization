# Example Usage of FlakeRanker

This example directory contains a `data` directory including the dataset of build jobs collected from the open-source project [Graphviz](https://gitlab.com/graphviz/graphviz) hosted on GitLab.

Results procuded during execution of FlakeRanker will be stored in the `results` directory.

## Step 0. Unzip Dataset

```bash
unzip data/jobs.zip data/
```

This command outputs the `data/jobs.csv` file.

## Step 1. Label Dataset with FlakeRanker

```bash
flakeranker label ./data/jobs.csv --output=./results/
```

This command outputs the `results/labeled_jobs.csv` file containing 2 additional columns:

- `flaky` (bool): Whether the job is flaky.
- `category` (str): The category label for flaky job failures.

## Step 2. Analyze Labeled Dataset with FlakeRanker

```bash
flakeranker analyze ./data/jobs.csv --output=./results/
```

This command outputs the `results/RFM.csv` file containing the following column for each identified `Category`:

- `Recency` (int): Recency value of the category calculated as described in RQ3-4.
- `Frequency` (int): Frequency value of the category as descibed in RQ1.
- `Monetary` (int): Monetary cost value of the category as calculated in RQ2.
