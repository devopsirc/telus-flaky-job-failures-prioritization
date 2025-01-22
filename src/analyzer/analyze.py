# This module takes as input a labeled dataset of flaky job failures.
# It analyzes the different categories of flaky job failures based on frequency, cost, and time evolution.

import pandas as pd

from src.core.config import settings
from src.utils import utils

# Read input data
df = pd.read_csv("../data/labeled_intermittent_failures.csv")

# Frequency Analysis
analysis_results = df["category"].value_counts().reset_index()
analysis_results.columns = ["category", "frequency"]


# Cost Analysis
## Machine Cost

machine_cost = df[["category", "duration"]].groupby("category").agg("sum").reset_index()
machine_cost.columns = ["category", "duration"]
machine_cost["machine_cost"] = (
    machine_cost["duration"] / 60
) * settings.CI_INFRA_PRICING_RATE  # by default duration is in seconds

analysis_results = (
    analysis_results.set_index("category")
    .join(machine_cost[["category", "machine_cost"]].set_index("category"))
    .reset_index()
)
analysis_results["machine_cost"] = analysis_results["machine_cost"].apply(lambda x: round(x, 2))

# %%
fig = px.bar(
    categories.sort_values("machine_cost", ascending=False).head(10),
    x="category",
    y="machine_cost",
    template="simple_white",
)
fig.update_layout(
    font_family="Rockwell",
    font_size=12,
    autosize=True,
    margin=dict(l=50, r=50, b=0, t=0, pad=0),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.95),
    width=1000,
)
fig.update_yaxes(
    showgrid=True,
)
fig.update_traces(
    textangle=0, textposition="outside", textfont_color="#a2a2a2", cliponaxis=False
)
fig.show(renderer="svg", config=config)

# %% [markdown]
# ### Diagnosis Cost

# %%
jobs = pd.read_csv("../data/jobs.csv")

# correct invalid values
jobs["created_at"] = pd.to_datetime(jobs["created_at"], format="mixed", utc=True)
jobs["finished_at"] = pd.to_datetime(jobs["finished_at"], format="mixed", utc=True)

# %% [markdown]
# Get rerun suites

# %%
grouped_jobs = (
    jobs[jobs["status"].isin(["success", "failed"])]
    .sort_values(by=["created_at"], ascending=True)
    .groupby(["project", "commit", "name"])
    .aggregate(
        {
            "id": list,
            "status": list,
            "created_at": list,
            "finished_at": list,
        }
    )
).reset_index()

grouped_jobs["count"] = grouped_jobs["id"].apply(lambda x: len(x))
flaky_reruns = grouped_jobs[
    grouped_jobs["status"].map(lambda x: set(["success", "failed"]).issubset(x))
].reset_index(drop=True)
flaky_reruns

# %%
flaky_reruns["count"].sum()

# %%
df_copy = df_copy.set_index("id")


# %%
def first_failure_finition_date(row):
    for i, status in enumerate(row["status"]):
        if status == "failed":
            return row["finished_at"][i]


def last_finition_date(row):
    return max(row["finished_at"])


def first_failure_category(row):
    for i, status in enumerate(row["status"]):
        if status == "failed":
            job_id = row["id"][i]
            if job_id in df["id"].to_list():
                return df_copy.loc[job_id, "category"]
            return None


# %%
flaky_reruns["category"] = flaky_reruns.apply(first_failure_category, axis=1)
flaky_reruns["first_failure_finished_at"] = flaky_reruns.apply(
    first_failure_finition_date, axis=1
)
flaky_reruns["last_job_finished_at"] = flaky_reruns.apply(last_finition_date, axis=1)
flaky_reruns = flaky_reruns[~flaky_reruns["category"].isnull()]
flaky_reruns["delay"] = (
    flaky_reruns["last_job_finished_at"] - flaky_reruns["first_failure_finished_at"]
)
flaky_reruns.head(1)

# %%
S = 0.6  # salary in $/min

diagnosis_cost = (
    flaky_reruns[["category", "delay"]].groupby("category").sum().reset_index()
)
diagnosis_cost["delay_min"] = diagnosis_cost["delay"].apply(
    lambda x: x.total_seconds() / 60
)  # convert delay in minutes
diagnosis_cost["diagnosis_cost"] = diagnosis_cost["delay_min"] * S
diagnosis_cost.sort_values("diagnosis_cost", ascending=False).head(10)

# %%
categories = (
    categories.set_index("category")
    .join(diagnosis_cost[["category", "diagnosis_cost"]].set_index("category"))
    .reset_index()
)
categories["diagnosis_cost"] = categories["diagnosis_cost"].apply(lambda x: round(x, 2))
categories["diagnosis_cost"] = categories["diagnosis_cost"].fillna(0)
categories.head(10)

# %%
fig = px.bar(
    categories.sort_values("diagnosis_cost", ascending=False).head(10),
    x="category",
    y="diagnosis_cost",
    template="simple_white",
)
fig.update_layout(
    font_family="Rockwell",
    font_size=12,
    autosize=True,
    margin=dict(l=50, r=50, b=0, t=0, pad=0),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.95),
    width=1000,
)
fig.update_yaxes(
    showgrid=True,
)
fig.update_traces(
    textangle=0, textposition="outside", textfont_color="#a2a2a2", cliponaxis=False
)
fig.show(renderer="svg", config=config)

# %% [markdown]
# ### Total Cost

# %%
categories["cost"] = categories["machine_cost"] + categories["diagnosis_cost"]

# %%
categories

# %%
categories.drop_duplicates(inplace=True)

# %%
categories["cost_rounded"] = categories["cost"].round()

# %%
plot_data = (
    categories.sort_values("cost", ascending=False)
    .head(20)
    .sort_values("cost")[["category", "cost", "machine_cost", "diagnosis_cost"]]
)
plot_data

# %%
plot_data = categories.sort_values("cost", ascending=False).head(20).sort_values("cost")
fig = px.bar(
    plot_data,
    y="category",
    x=["diagnosis_cost", "machine_cost"],
    template="simple_white",
    labels={
        "variable": "",
        "value": "Total Cost ($)",
        "category": "",
        "diagnosis_cost": "Diagnosis Cost",
        "machine_cost": "Machine Cost",
    },
    color_discrete_sequence=[
        px.colors.qualitative.G10[0],
        px.colors.qualitative.G10[1],
    ],
    orientation="h",
)
fig.update_traces(width=0.7)

fig.add_trace(
    go.Scatter(
        y=plot_data["category"],
        x=plot_data["cost_rounded"],
        text=(plot_data["cost_rounded"]).map("  ${:,.0f}".format),
        mode="text",
        textposition="middle right",
        textfont=dict(size=15, color="#a2a2a2"),
        showlegend=False,
    )
)

fig.update_layout(
    font_family="Rockwell",
    font_size=15,
    autosize=True,
    margin=dict(l=0, r=2, b=0, t=1, pad=0),
    legend=dict(yanchor="top", y=0.2, xanchor="left", x=0.6, traceorder="reversed"),
    width=780,
    height=470,
)

fig.update_xaxes(
    showline=True,
    showgrid=True,
    linewidth=1,
    range=[0, 550000],
    linecolor="black",
    mirror=True,
    ticks="outside",
)
fig.update_yaxes(
    showline=True,
    showgrid=False,
    linewidth=0,
    linecolor="black",
    mirror=True,
    showticklabels=True,
)
"""
fig.update_traces(
    textangle=0, textposition="outside", textfont_color="#a2a2a2", cliponaxis=False, width=.7
)
"""
fig.show(renderer="svg", config=config)

# %%
categories.drop(columns=["cost_rounded"], inplace=True)
categories.head(3)

# %%
categories["diagnosis_cost_proportion"] = (
    categories["diagnosis_cost"] * 100 / categories["cost"]
).apply(lambda x: round(x, 2))

# %%
top20_costly = categories.sort_values("cost", ascending=False).head(20)
top20_costly.loc[top20_costly["diagnosis_cost_proportion"].idxmin(), :]

# %%
top20_costly.loc[top20_costly["diagnosis_cost_proportion"].idxmax(), :]

# %%
categories.to_csv("./results/categories.csv", index=False)

# %% [markdown]
# ## Analysis of Evolution in Time (Trends)

# %%
df

# %% [markdown]
# We group the jobs by `category` and `created_at` to identify the number of jobs per day and by category

# %%
df_copy = df.copy(deep=True)
df_copy["created_at"] = pd.to_datetime(df_copy["created_at"], format="mixed", utc=True)
df_copy["date"] = df_copy["created_at"].apply(lambda t: t.to_pydatetime().date())
categories_trends = (
    df_copy[["id", "date", "category"]]
    .groupby(["date", "category"])
    .count()
    .reset_index()
)
categories_trends.columns = ["date", "category", "count"]
categories_trends.head(5)

# %% [markdown]
# We add the `empty_logs` category to better interpret the gaps

# %%
jobs = pd.read_csv("../data/jobs.csv")
jobs["created_at"] = pd.to_datetime(jobs["created_at"], format="mixed", utc=True)
jobs["finished_at"] = pd.to_datetime(jobs["finished_at"], format="mixed", utc=True)

# %%
empty_logs = pd.read_csv("../data/intermittent_failures.csv")
empty_logs = empty_logs[empty_logs["log"].isnull()]
empty_logs = (
    empty_logs[["id", "log"]]
    .set_index("id")
    .join(jobs.set_index("id"))
    .reset_index()[["id", "created_at", "log"]]
)
empty_logs

# %% [markdown]
# We select the `n` most frequent categories

# %%
n = 20

n_top_frequent_categories = (
    categories.sort_values("count", ascending=False).head(n)["category"].to_list()
)

# %% [markdown]
# We plot the evolution of the number of job over time by category

# %%
import importlib
from src.utils import vizualization as viz

importlib.invalidate_caches()
importlib.reload(viz)

data = [empty_logs] + [
    df[df["category"] == cat].copy() for cat in n_top_frequent_categories
][::-1]
titles = ["missing_logs"] + n_top_frequent_categories[::-1]
modes = ["markers"] * (n + 1)

colors = (
    ["#d3d3d3"]
    + px.colors.qualitative.G10_r
    + px.colors.qualitative.Dark2_r
    + px.colors.qualitative.Plotly * 3
)
start_date = "2018-02-01"
end_date = "2024-07-11"


def plot_count_timeseries(
    data: list[pd.DataFrame],
    titles: list[str],
    modes: list[str],
    colors: list[str],
    start_date: str,
    end_date: str,
    width: int = 1500,
    height: int = 300,
):
    """Plot count timeseries of dataframe on the same figure."""
    # add the figure traces
    plot_data = []
    y_values = []
    for i, df in enumerate(data):
        count_ts = viz.to_count_ts(df)
        count_ts["timestamp"] = pd.to_datetime(count_ts["date"])
        count_ts = count_ts[
            (count_ts["timestamp"] >= start_date) & (count_ts["timestamp"] <= end_date)
        ]
        y_values.append(i + 1)
        # add the time series as a line chart
        plot_data.append(
            go.Scatter(
                x=count_ts["date"],
                y=[i + 1] * count_ts.shape[0],
                mode=modes[i],
                marker=dict(size=7, color=colors[i]),
                line=dict(width=1, color=colors[i]),
                showlegend=True,
                name=titles[i],
                line_shape="spline",
                line_smoothing=0.3,
                # marker_symbol='line-ns-open',
            )
        )
    layout = go.Layout(
        font_family="Rockwell",
        font_size=15,
        font_color="black",
        autosize=False,
        margin=dict(l=280, r=1, b=0, t=1, pad=10),
        showlegend=False,
        legend=dict(
            xanchor="center",
            x=0.5,
            orientation="h",
            entrywidth=0.5,
            entrywidthmode="fraction",
            traceorder="reversed",
        ),
        width=width,
        height=height,
        template="plotly_white",
    )
    # show the figure
    fig = go.Figure(data=plot_data, layout=layout)
    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
        ticks="outside",
        ticklabelmode="period",
        minor=dict(ticks="inside", showgrid=True),
    )
    fig.update_yaxes(
        showline=True,
        showgrid=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
        ticks="outside",
        showticklabels=True,
        tickmode="array",
        tickvals=y_values,
        ticktext=titles,
    )
    fig.show(renderer="svg", config=config)


plot_count_timeseries(
    data, titles, modes, colors, start_date, end_date, width=800, height=550  # 670, 450
)

# %%
categories.to_csv("./results/categories.csv", index=False)

# %%
