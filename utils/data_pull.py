"""Functions to return API friendly date ranges
"""

import pandas as pd


def account_activity(qtrade, account_id, date_range):
    """
    Returns a df with all qtrade account activity within some input date range.
    """
    df = pd.DataFrame(
        qtrade.get_account_activities(account_id, date_range[0][0], date_range[0][1])
    )
    if len(date_range) == 1:
        return df

    for dates in date_range[1:]:
        df = df.append(
            pd.DataFrame(qtrade.get_account_activities(account_id, dates[0], dates[1]))
        )

    return df
