# This module takes as input a full dataset of jobs including labeled flaky jobs.
# It analyzes the different categories of flaky job failures based on frequency, cost, and time evolution.
#
# Required fields: id, name, commit, project, status, duration, created_at, finished_at, category

import sys
import pandas as pd

from src.flakeranker.analyzer import utils as analyzer_utils
from src.flakeranker import utils


def run(input_file_path: str, output_file_path: str):
    """Takes as input the path to full `.csv` jobs dataset including labeled flaky jobs. Output of the `labeler`.

    Outputs: `categories.csv` including analysis results for each failure category as presented in the following columns.

        `category`: The failure category.
        `frequency`: Frequency of the category, i.e. number of jobs.
        `machine_cost`: Machine cost component value for the category, as described in the original paper.
        `diagnosis_cost`: Diagnosis cost component value for the category, as described in the original paper.
        `cost`: Estimated total cost for the category, as described in the original paper.
        `recency`: Recency value of the category, as computed in the original paper. The number of last jobs considered is parameterizable using the `RECENCY_N_LAST` env. variable.
    """
    # Read input data
    jobs = pd.read_csv(input_file_path)

    # preprocessing
    jobs["created_at"] = pd.to_datetime(jobs["created_at"], format="mixed", utc=True)
    jobs["finished_at"] = pd.to_datetime(jobs["finished_at"], format="mixed", utc=True)
    labeled_flaky_jobs = jobs[jobs["flaky"] & jobs["status"] == "failed"]

    ##########################
    #        Frequency       #
    ##########################
    categories = labeled_flaky_jobs["category"].value_counts().reset_index()
    categories.columns = ["category", "frequency"]

    ##########################
    #      Monetary Cost     #
    ##########################
    # Machine
    machine_costs = analyzer_utils.compute_categories_machine_costs(labeled_flaky_jobs)
    categories = utils.join_dfs(categories, machine_costs)
    # Diagnosis
    diagnosis_costs = analyzer_utils.compute_categories_diagnosis_costs(
        jobs, labeled_flaky_jobs
    )
    categories = utils.join_dfs(categories, diagnosis_costs)
    # Total Cost
    categories["cost"] = (
        categories["machine_cost"] + categories["diagnosis_cost"]
    ).round()
    categories.drop_duplicates(inplace=True)

    ##########################
    #         Recency        #
    ##########################
    recencies = analyzer_utils.compute_categories_recencies(labeled_flaky_jobs)
    categories = utils.join_dfs(categories, recencies)

    # Export
    categories.to_csv(output_file_path, index=False)


if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]
    run(input, output)
