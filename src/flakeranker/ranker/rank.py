"""Module for ranking flaky job failure categories based on RFM measures, i.e. Output of Analyzer."""

import sys
import numpy as np
import pandas as pd
from tqdm import trange
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest


def find_outliers(rfm: pd.DataFrame):
    IF = IsolationForest(n_estimators=500, contamination=0.1)
    IF.fit(rfm[["recency", "frequency", "cost"]])
    IF_anomalies = IF.predict(rfm[["recency", "frequency", "cost"]])
    outliers = rfm[IF_anomalies == -1]
    return outliers


def preprocess(rfm: pd.DataFrame) -> pd.DataFrame:
    outliers = find_outliers(rfm)
    outliers.to_csv("outliers.csv", index=False)

    # remove outliers
    rfm = rfm[~rfm["category"].isin(outliers["category"])]

    # RFM Scoring
    rfm["R"] = pd.qcut(rfm["recency"], q=5, labels=list(range(5, 0, -1)))
    rfm["F"] = pd.qcut(rfm["frequency"], q=5, labels=list(range(1, 6)))
    rfm["M"] = pd.qcut(rfm["cost"], q=5, labels=list(range(1, 6)))

    return rfm


def rank(input_file_path: str, output_file_path: str):
    # Read input data
    rfm = pd.read_csv(input_file_path)[["category", "recency", "frequency", "cost"]]
    rfm_scores = preprocess(rfm)

    y = rfm_scores["category"]
    X = rfm_scores.drop(columns=["category"]).astype(int)

    inertias = []
    models = []
    for _ in trange(500, desc="Fitting clustering models"):
        kmeans = KMeans(n_clusters=8, init="k-means++")
        kmeans.fit(X)
        models.append(kmeans)
        inertias.append(kmeans.inertia_)

    i = np.argmin(inertias)
    print(f"Lowest clustering inertia: {min(inertias)}")

    model = models[i]

    df_cluster = pd.DataFrame(X).astype(int)
    df_cluster["cluster"] = model.labels_
    df_cluster["category"] = y
    df_cluster["Recency"] = rfm["Recency"]
    df_cluster["Frequency"] = rfm["Frequency"]
    df_cluster["Monetary"] = rfm["Monetary"]
    df_cluster.head()


if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]
    rank(input, output)
