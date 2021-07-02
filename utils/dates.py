"""Functions to return API friendly date ranges
"""
import datetime
import math


def end_of_month(date):
    """
    For input date, return a date object for the last day of the month.
    """
    next_month = date.month + 1
    if next_month == 13:
        return date.replace(year=date.year + 1, month=1) - datetime.timedelta(days=1)

    return date.replace(month=next_month) - datetime.timedelta(days=1)


def qtrade_date_range(start, end=datetime.date.today()):
    """
    function to return a list of tuples, each with a
    start and end date that are valid inputs to qtrade's
    API. Being, a single month start and end
    """
    if isinstance(start, str):
        start = datetime.date.fromisoformat(start)
    elif not isinstance(start, datetime.datetime):
        raise "Please pass in a string of format 'YYYY-MM-DD' or a datetime object"

    if isinstance(end, str):
        end = datetime.date.fromisoformat(end)
    elif not isinstance(end, datetime.date):
        raise "Please pass in a string of format 'YYYY-MM-DD' or a datetime object"

    # Create tupples for each month between start and end:
    last_day = end_of_month(start)
    container = [(start.strftime("%Y-%m-%d"), last_day.strftime("%Y-%m-%d"))]

    while last_day < end:
        next_day = last_day + datetime.timedelta(days=1)
        last_day = end_of_month(next_day)
        container.append((next_day.strftime("%Y-%m-%d"), last_day.strftime("%Y-%m-%d")))

    return container


# create date object
def dates_of_interest(cadence, start, end):
    if isinstance(start, str):
        start = datetime.date.fromisoformat(start)
    elif not isinstance(start, datetime.datetime):
        raise "Please pass in a string of format 'YYYY-MM-DD' or a datetime object"

    if isinstance(end, str):
        end = datetime.date.fromisoformat(end)
    elif not isinstance(end, datetime.date):
        raise "Please pass in a string of format 'YYYY-MM-DD' or a datetime object"

    if cadence == "yearly":
        return yearly_bins(start, end)
    elif cadence == "quarterly":
        return quarterly_bins(start, end)
    elif cadence == "monthly":
        return monthly_bins(start, end)
    elif cadence == "daily":
        return daily_bins(start, end)
    else:
        raise ValueError("Cadence must be yearly, quarterly, monthly, or daily")


def yearly_bins(start, end):
    dates = {}
    start_yr = start.year
    end_yr = end.year

    while start_yr <= end_yr:
        dates[f"{start_yr}"] = {
            "start": f"{start_yr}-01-01",
            "end": f"{start_yr}-12-31",
        }
        start_yr += 1

    return dates


def quarterly_bins(start, end):
    dates = {}
    start_q = f"{start.year}{math.ceil(start.month/3)}"
    end_q = f"{end.year}{math.ceil(end.month/3)}"

    while start_q <= end_q:
        if start_q[-1] == "4":
            nxt_q = f"{int(start_q[:4])+1}1"
        else:
            nxt_q = f"{start_q[:4]}{int(start_q[-1])+1}"
        nxt_q_month = datetime.date.fromisoformat(
            f"{nxt_q[:4]}-{str(int(nxt_q[-1])*3-2).zfill(2)}-01"
        )
        dates[f"{start_q[:4]}Q{start_q[-1]}"] = {
            "start": f"{start_q[:4]}-{str(int(start_q[-1])*3-2).zfill(2)}-01",
            "end": (nxt_q_month + datetime.timedelta(days=-1)).strftime("%Y-%m-%d"),
        }
        start_q = nxt_q

    return dates


def monthly_bins(start, end):
    dates = {}
    start_m = start.strftime("%Y-%m")
    end_m = end.strftime("%Y-%m")

    while start_m <= end_m:
        nxt_mnth = datetime.date.fromisoformat(f"{start_m}-01") + datetime.timedelta(
            days=31
        )
        dates[start_m] = {
            "start": f"{start_m}-01",
            "end": (nxt_mnth + datetime.timedelta(days=-1)).strftime("%Y-%m-%d"),
        }
        start_m = nxt_mnth.strftime("%Y-%m")

    return dates


def daily_bins(start, end):
    dates = {}

    while start <= end:
        dates[start.strftime("%Y-%m-%d")] = {
            "start": start.strftime("%Y-%m-%d"),
            "end": start.strftime("%Y-%m-%d"),
        }
        start += datetime.timedelta(days=1)

    return dates
