"""Functions to return balance and position summary
"""
import pandas as pd
from typing import Tuple


def retrieve_balance_positions(
    qtrade, account_id, targets, pcnt_multiplier
) -> Tuple[pd.DataFrame, int]:
    """
    Function to organize account balances and positions based on
    an incoming target portfolio percentage.
    """

    # targets must contain a key for "Other":
    assert "Other" in targets, "must have an 'Other' key in targets, even if it's zero"

    positions = qtrade.get_account_positions(account_id=account_id)
    balances = qtrade.get_account_balances(account_id=account_id)

    # For simplicity, we use combined balances, which is an apporximation
    # that the user must deal with...
    combinedBalanceCAD = 0
    combinedBalanceUSD = 0

    for balance in balances["combinedBalances"]:
        if balance["currency"] == "CAD":
            combinedBalanceCAD = balance["cash"]
        elif balance["currency"] == "USD":
            combinedBalanceUSD = balance["cash"]

    exchangeUSDtoCAD = combinedBalanceCAD / combinedBalanceUSD

    # Now use targets to find their amounts:
    market_total = 0
    summary = {key: [0] for key in targets.keys()}

    # Identify current market value of positions
    for position in positions:
        if position["openQuantity"] > 0:
            if position["symbol"] in targets.keys():
                if "." not in position["symbol"]:
                    summary[position["symbol"]] = [
                        position["currentMarketValue"] * exchangeUSDtoCAD
                    ]
                else:
                    summary[position["symbol"]] = [position["currentMarketValue"]]
                market_total += summary[position["symbol"]][0]
            else:
                summary["Other"][0] += position["currentMarketValue"]
                market_total += position["currentMarketValue"]

    # Organize data against targets
    for symbol, amount in summary.items():
        summary[symbol] = [
            amount[0],
            amount[0] / market_total * 100,
            targets[symbol],
            targets[symbol] - amount[0] / market_total * 100,
            targets[symbol]
            + pcnt_multiplier * (targets[symbol] - amount[0] / market_total * 100),
        ]

    # Create df with purchase amount suggestion
    df_summary = pd.DataFrame.from_dict(
        summary,
        orient="index",
        columns=[
            "Amount (CAD)",
            "Current Pcnt",
            "Tagert Pcnt",
            "Pcnt Difference",
            "Target + Pcnt Diff",
        ],
    )
    sum_target = df_summary[df_summary["Target + Pcnt Diff"] > 0][
        "Target + Pcnt Diff"
    ].sum()
    df_summary["Weight"] = df_summary["Target + Pcnt Diff"].apply(
        lambda x: x / sum_target if x > 0 else 0
    )
    df_summary["Purchase amount (CAD)"] = df_summary["Weight"] * combinedBalanceCAD

    return df_summary, combinedBalanceCAD
