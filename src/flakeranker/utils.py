"""Utilities for FlakeRanker."""

import pandas as pd


def join_dfs(df1: pd.DataFrame, df2: pd.DataFrame, key: str = "category"):
    """Join two dataframes on a shared column key, defaults to `category.`"""
    return df1.set_index(key).join(df2.set_index(key)).reset_index()
