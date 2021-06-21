# my-qtrade-dashboard
This repository holds my investment thesis, market notes, and financial dashboard, using [qtrade](https://pypi.org/project/qtrade/).

## Investment Thesis
1. Buy and hold -> invest money that can be left for 10+ years.
2. Assume markets are efficient & rational -> low cost market-wide index investing. Skew to small-cap value stocks.
3. Use [Shiller PE ratio](https://www.multpl.com/shiller-pe) to determine if market is hot or cold. Adjust holdings/index's tracked accordingly. i.e., hot market should influence a larger bond holding. Cold market should influence a larger equities holding.

This investment thesis is mostly shaped by the [Rational Reminder podcast](https://rationalreminder.ca/).

## Human Capital
Human capital is the expected return from one's career.

For example, those who work in financial services receive above average financial capital, but are high risk of losing their jobs when a recession hits. As such, their human capital looks a lot like equities, and they should consider a skewed portfolio to bonds. Conversely, those who work in, say, energy or government funded childhood education have safer jobs. Their human capital looks a lot like a bond, so they should skew to equities in their portfolio. It might even make sense to leverage their credit worthiness to compensate for the bond-like nature of their human capital.

Knowing ones human capital is critical to determining their investment strategy.

## What are you investing for?
Investments should be bucketed to clearly define the responsibility of that money. Common buckets include:
* Rainy day (typically 6+ months of cash to pay for monthly expenses - stored in high interest savings accounts)
* Housing
* Education (yourself or dependancies)
* Retirement
* Vacations

Knowing what your money will be used for, and when you'll need it should determine how it is invested. The longer the time horizon, and the more risk your investment strategy can take on.

Your rainy day bucket should always be the first one maxed out. Do not touch this money until a rainy day arrives. Periodically update this bucket's size depending on your life situation.

## Margin vs TFSA
To tax benefits from a TFSA make it the preferred vehicle for assets you plan to adjust periodically. That is, if you're buying stocks that you aren't planning to hold forever, you should do so in a TFSA.

Long term investments in a margin accounts (no tax sheltering), should rebalance themselves, without the need for you to sell your position and trigger captial gains. ETFs and mutual funds are the ideal mechanism for this.

## My EFT Picks
* XEI -> Cad Dividend
* WSRD/WSRI -> wealth simple socially responsible ETFs 
* VVL -> Global value 
* ZRE -> Cad REIT 
* ZLB -> Cad Low Volitility 
* ZAG -> Diversified Cad Bonds (gov & corp) 
* PZD -> Clean tech
* ICLN/FAN -> Clean energy
* VOE/VBR -> small/mid cap US value
* VTI -> Total market

## Monthly deposit:
* XEI/WSRD/WSRI/VVL/ZLB/ZRE/ZAG + VOE/VBR/ICLN/FAN/PZD/VTI

## How the dashboard works?
First, add you Qtrade authorization token as an environment variable named ``qtrade_token``:
```sh
export qtrade_token=<token_value>
```

Using [Stremlit](https://docs.streamlit.io/en/stable/getting_started.html), simply run:
```bash
streamlit run first_app.py
```

## WORK IN PROGRESS
Clean up functions and instructions for others to use :)
i.e., requirements need fixing (streamlit==0.82.0 works with bokeh=2.2.0)


## Next up:
- Dividend total for the displayed period
- Available cash! (just cause it's a simple call)
- Portfolio balance, built by summing activity!! -> cash & stock amount 
    - What is my total deposit amount? It should equal my TFSA limit yeah?
- Commission % as an average of the total balance over the period ((start + end) / 2)
- Current dividend yields (as a percentage of account balance) -> using "get account positions" & ticker info
    - Ohhh, build up a "total investment" vs "dividend payout" view :) 
- Portfolio performance via account activity, buy & sell price, remaining units, and current value of those units.
    - Maybe even build a comparison to 
- Cash contributions and returns (time windowed)
- Stock pick checklist
- Ticker tracker summary -> stocks of interest to monitor
- Market sentiment analysis
- Individual stock analysis (like: https://github.com/antonio-catalano/StockAnalysisApp)
- Caching
- Better display of data

## Finished:
1. Structure of dashboards (defined above, see `first_app.py`) -> simple for now
2. Authoriztions & token refresh workflow.
3. Portolio dividend history
4. Trade activity & commissions
