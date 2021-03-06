"""Functions to return API friendly date ranges
"""
import datetime


def end_of_month(date):
    """
    For input date, return a date object for the last day of the month.
    """
    next_month = date.month + 1
    if next_month == 13:
        return date.replace(year = date.year + 1, month = 1) - datetime.timedelta(days=1)
    
    return date.replace(month = next_month) - datetime.timedelta(days=1)
    

def qtrade_date_range(start, end = datetime.date.today()):
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
