"""Utilities functions."""

import holidays
from datetime import datetime, timedelta

# Canada, ON Holidays
CA_HOLIDAYS = holidays.country_holidays("CA", subdiv="ON")


def compute_job_deltas(row):
    """Returns the list of time gaps in seconds between jobs' finition and creation timestamps."""
    deltas = []
    for i in range(1, len(row["created_at"])):
        # delta diagnosis and fix time between the last finished job and this job creation.
        start_date = row["finished_at"][i - 1]
        end_date = row["created_at"][i]
        delta = (end_date - start_date).total_seconds()
        # w = count_weekend_and_holidays(start_date, end_date)
        deltas.append(delta) # add delta minus weekend and holidays in seconds

    return deltas


def compute_time_deltas(date_times: list[datetime]):
    """Return time gaps from an array of timestamps."""
    date_times.sort()
    deltas = []
    for i in range(1, len(date_times)):
        delta = (date_times[i] - date_times[i - 1]).total_seconds()
        deltas.append(delta)

    return deltas


def count_weekend_and_holidays(start_date, end_date):
    # Initialize a counter for weekend days
    weekend_holidays = 0
    # Iterate through each day in the date range
    current_date = start_date + timedelta(days=1)
    while current_date < end_date:
        if (current_date.weekday() in [5, 6]) or (current_date in CA_HOLIDAYS) :  # 5 = Saturday, 6 = Sunday
            weekend_holidays += 1
        current_date += timedelta(days=1)

    return weekend_holidays

def seconds_to_human_readable(seconds: int):
    """Convert seconds to human readable string."""
    intervals = (
        ("years", 60 * 60 * 24 * 365),  # 60 * 60 * 24 * 365
        ("months", 60 * 60 * 24 * 30),  # 60 * 60 * 24 * 30
        ("weeks", 60 * 60 * 24 * 7),  # 60 * 60 * 24 * 7
        ("days", 60 * 60 * 24),  # 60 * 60 * 24
        ("hours", 3600),  # 60 * 60
        ("minutes", 60),
        ("seconds", 1),
    )
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds %= count
            if value == 1:
                name = name.rstrip("s")  # singular form if value is 1
            result.append(f"{value} {name}")

    return ", ".join(result)
