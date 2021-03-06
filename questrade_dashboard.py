import os
import datetime

# Cheatsheet here: https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py
import streamlit as st
import numpy as np
import pandas as pd
from qtrade import Questrade

from utils import qtrade_date_range, dates_of_interest, account_activity

st.title("My Questrade Dashboard")

# Authenticate
st.write("Welcome! Let's start by authenticating you and your account.")
qtrade_token = "qtrade_token"
overwrite_token = st.text_input("Should we look somewhere other than 'qtrade_token'?")
if overwrite_token:
    qtrade_token = overwrite_token
st.write(f"Looking for a qtrade token in env variable: {qtrade_token}")
try:
    qtrade = Questrade(access_code=os.getenv(qtrade_token))
    aapl, amzn = qtrade.ticker_information(["AAPL", "AMZN"])
    st.write("Authorization sucessful via qtrade_token")
except:
    try:
        qtrade = Questrade(token_yaml="access_token.yml")
        aapl, amzn = qtrade.ticker_information(["AAPL", "AMZN"])
        st.write("Authorization sucessful via access_token")
    except:
        try:
            qtrade.refresh_access_token(
                from_yaml=True, yaml_path="access_token.yml"
            )  # When Qtrade refreshes token, it kills the old credentials
            aapl, amzn = qtrade.ticker_information(["AAPL", "AMZN"])
            st.write("Authorization sucessful via refreshed access_token")
        except:
            st.write(f"ERROR: was unable to authenticate user")

# Select an account!
"""
## Account selection
By default, we use the first account we can find. 
You can override that below with either an index,
or the account ID itself:
"""
# Pull accounts
account_ids = qtrade.get_account_id()
input_index = st.text_input(
    "Would you prefer to use a different account index (default is 0)?"
)
input_id = st.text_input(
    "Would you prefer to set the account ID (default is 0th index returned by API)?"
)
if input_id:
    acct_id = input_id
elif input_index:
    acct_id = account_ids[int(input_index)]
else:
    acct_id = account_ids[0]


# Retreive all data
"""
## Retrieve data
By default, retrieves all year-to-date data.
"""
end = datetime.date.today()
start = end.replace(month=1, day=1).strftime("%Y-%m-%d")
end = end.strftime("%Y-%m-%d")

overwrite_start = st.text_input(
    "Overwrite default start date (format must be 'YYYY-MM-DD'):"
)
if overwrite_start:
    start = overwrite_start
overwrite_end = st.text_input(
    "Overwrite default end date (format must be 'YYYY-MM-DD'):"
)
if overwrite_end:
    end = overwrite_end

st.write(f"Data retrieval window from {start} to {end}")

# Date range:
date_range = qtrade_date_range(start=start, end=end)
# Account activity:
activity = account_activity(qtrade=qtrade, account_id=acct_id, date_range=date_range)

# Clean dates
# settlement date is the same as transaction (almost always for me),
# and tradeDate is most commonly the same too (I always buy "market")
activity = activity.drop(columns=["tradeDate", "settlementDate"])
activity = activity.rename(columns={"transactionDate": "date"})
activity[["date"]] = activity[["date"]].apply(
    pd.to_datetime, **{"utc": True, "infer_datetime_format": True}
)  # convert to datetime objects
activity["date"] = activity["date"].dt.date  # keep only the date
activity[["date"]] = activity[["date"]].apply(
    pd.to_datetime, **{"infer_datetime_format": True}
)  # convert to datetime (without tz)
activity = activity.reset_index()

st.dataframe(activity.head(5))
cat = activity.groupby("type")


## Remaining content to migrate:
"""
# Dividend History
"""
option = st.sidebar.selectbox(
    "What cadence would you like to view data in?",
    ["daily", "monthly", "quarterly", "yearly"],
    index=2,
)

"Dividend cadence:", option

div = activity.loc[cat.groups["Dividends"]]

bins = dates_of_interest(cadence=option, start=start, end=end)
yr_bins = []
div_bins = []
for yr, value in bins.items():
    mask = (div["date"] >= value["start"]) & (div["date"] <= value["end"])
    div_bins.append(div.loc[mask]["netAmount"].agg(np.sum))
    yr_bins.append(yr)

# Categories: https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html
from bokeh.models.tools import BoxZoomTool, ResetTool
from bokeh.plotting import figure

p = figure(x_range=yr_bins, tools=[BoxZoomTool(), ResetTool()], plot_width=800)

p.vbar(x=yr_bins, top=div_bins, width=0.9)

p.xgrid.grid_line_color = None
p.y_range.start = 0

st.bokeh_chart(p, use_container_width=True)

"""
# Trade Volume
"""
"trades cadence:", option

trades = activity.loc[cat.groups["Trades"]]
# https://pandas.pydata.org/pandas-docs/stable/getting_started/comparison/comparison_with_sql.html
trades.groupby("action").size()
# trades.query("grossAmount > 0")
yr_bins = []
sell_bins = []
buy_bins = []

for yr, value in bins.items():
    # Sell orders
    mask_sell = (
        (trades["date"] >= value["start"])
        & (trades["date"] <= value["end"])
        & (trades["action"] == "Sell")
    )
    sell_bins.append(trades.loc[mask_sell]["grossAmount"].agg(np.sum))
    # Buy orders
    mask_buy = (
        (trades["date"] >= value["start"])
        & (trades["date"] <= value["end"])
        & (trades["action"] == "Buy")
    )
    buy_bins.append(trades.loc[mask_buy]["grossAmount"].agg(np.sum) * -1)
    # Year bins
    yr_bins.append(yr)

# https://www.tutorialspoint.com/how-can-bokeh-be-used-to-visualize-multiple-bar-plots-in-python
from bokeh.plotting import figure
from bokeh.transform import dodge

labs = yr_bins
vals = ["Buy", "Sell"]
my_data = {"labs": labs, "Buy": buy_bins, "Sell": sell_bins}

fig = figure(
    x_range=labs, plot_width=800, plot_height=800, tools=[BoxZoomTool(), ResetTool()]
)
fig.vbar(
    x=dodge("labs", -0.25, range=fig.x_range),
    top="Buy",
    width=0.2,
    source=my_data,
    color="green",
)
fig.vbar(
    x=dodge("labs", 0.0, range=fig.x_range),
    top="Sell",
    width=0.2,
    source=my_data,
    color="red",
)

st.bokeh_chart(fig, use_container_width=True)


"""
## Cost of Commissions over that period:
"""

st.dataframe(trades.groupby("action").agg({"commission": np.sum}))
