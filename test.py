import os
import logging

from qtrade import Questrade

from utils import qtrade_date_range, sum_dividend

# Set up console logging:
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
LOG.addHandler(ch)

# Create Questrade object either through new token (one time use)
# provided by Questrade, or the access_token.yaml.
try:
    qtrade = Questrade(access_code=os.getenv("qtrade_token"))
    aapl, amzn = qtrade.ticker_information(['AAPL', 'AMZN'])
    LOG.info("Authorized via qtrade_token")
except: 
    try:
        qtrade = Questrade(token_yaml="access_token.yml")
        aapl, amzn = qtrade.ticker_information(['AAPL', 'AMZN'])
        LOG.info("Authorized via access_token")
    except:
        try:
            qtrade.refresh_access_token(from_yaml=True) # When Qtrade refreshes token, it kills the old credentials
            aapl, amzn = qtrade.ticker_information(['AAPL', 'AMZN'])
            LOG.info("Authorized via refreshed access_token")
        except:
            LOG.error("Authorized was unsuccessful")

# Pull accounts
account_ids = qtrade.get_account_id()

#Total tfsa dividends:
date_range = qtrade_date_range("2018-03-01") # first month of dividends was 2018-03-01
print(sum_dividend(qtrade, account_ids[1], date_range))
