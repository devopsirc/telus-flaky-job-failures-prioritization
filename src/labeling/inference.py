import re


def infer_category(row, patterns):
    """Infer job category and subcategory based on manual patterns."""
    if row["category"] is not None:
        return row["category"], row["subcategory"]
    if row["failure_reason"] == "stuck_or_timeout_failure":
        return "limits_exceeded", row["failure_reason"]
    for _, pattern in patterns.iterrows():
        logs = row["log"]
        if re.search(pattern["regex"], logs, flags=re.IGNORECASE) is not None:
            return pattern["category"], pattern["subcategory"]
    return None, None


def infer(df, output: str):
    """Automatically assing jobs to categories and subcategories based on manual regex patterns"""
    df["category"], df["subcategory"] = zip(*df.apply(infer_category, axis=1))
    df.to_csv(output, index=False)

    # Check the obtained coverage
    n_clustered = df[~df["category"].isna()].shape[0]
    print(f"{round(float(n_clustered / df.shape[0]) * 100, 2)}% of jobs are assigned")
