"""Functions to return dividend amounts
"""
from typing import List


def sum_dividend(qtrade, account_id, date_range)->float:
    """
    Function to sum dividends within a particular date range 
    given the input account_id
    """
    dividend_total = 0
    for dates in date_range:
        activities = qtrade.get_account_activities(account_id, dates[0], dates[1])
        dividends = [rec for rec in activities if rec["type"]=="Dividends"]
        dividend_total += sum_list([rec["netAmount"] for rec in dividends])
    
    return dividend_total

def sum_list(list_in: List)->float:
    total: float = 0
    for val in list_in:
        total += val
    return total
