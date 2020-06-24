# my-qtrade-dashboard

This repo will house the code I use to construct a financial dashboard, using [qtrade](https://pypi.org/project/qtrade/).

Should I use Jupyter labs or [Streamlit](https://www.streamlit.io/)?

## content:
- Portolio dividend history
- Current dividend yields 
- Ticker tracker summary
- Portfolio summary & comparison to target
- Market sentiment analysis 

## Trading strategy:
Sunday run:
- Compare ETF & market sentiment (what Sami showed me & the shiller index) to determine if the market is hot or cold
    - Candlestick OHLC data points -> moving averages 
- When the market is Hot, look to reduce positions that are bloated 
- When the market is cold, look to open positions that are valuable

## Margin vs TFSA
- TFSA should have less activity, and less stocks -> set it and forget it (80/20)
- Margin should be where more trading strategy takes place (80/20)
