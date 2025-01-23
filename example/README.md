# Example Usages of Flaky Ranker

This example directory contains a `data` directory including the dataset of build jobs collected from the GraphViz project on GitLab.

Results procuded during execution of FlakeRanker will be stored in the `results` directory.

## Step 1. Unzip Dataset

```bash
unzip data/graphviz.zip data/
```

This command outputs the `data/graphviz.csv` file.

## Step 1. Label Dataset with FlakeRanker

```bash
flakeranker label ./data/graphviz.csv --output=./results/
```

This command outputs the `results/labeled_graphviz.csv` file containing 2 additional columns:

- `flaky` (bool): Whether the job is flaky.
- `category` (str): The category label for flaky job failures.

## Step 2. Analyze Labeled Dataset with FlakeRanker

```bash
flakeranker analyze ./data/graphviz.csv --output=./results/
```

This command outputs the `results/labeled_graphviz.csv` file containing 2 additional columns:

- `flaky` (bool): Whether the job is flaky.
- `category` (str): The category label for flaky job failures.
