import yfinance as yf
import pandas as pd

def get_last_price(ticker):
    return yf.Ticker(ticker).history().tail(1)['Close'].iloc[0]

def get_price_at(ticker, date):
    return yf.Ticker(ticker).history(date)['Open']

# start and end in "YEAR-MO-DA" format, with 0s in front
def get_historical_data(tickers, start, end):
    data = yf.download(tickers, start=start,
                       end=end, group_by='tickers')

    series = {ticker : data[ticker]['Open'] for ticker in tickers}

class Simulation:

    def __init__(this, portfolio, date=None):
        this.portfolio = portfolio
        if date:
            this.date = date
        else:
            today = pd.Timestamp.today()
            this.date = '%i-%i-%i' % (today.year, today.month, today.day)
        this.deposit = this.value()

    def value(this):
        return sum([shares * get_price_at(ticker, this.date) for ticker, shares in this.portfolio.items()])

    def gains(this):
        return this.deposit - this.value()

    def present_value(this):
        return sum([shares * get_last_price(ticker) for ticker, shares in this.portfolio.items()])

    def present_gains(this):
        return this.deposit - this.present_value()

    def buy_stocks(this, stocks):
        for ticker, shares in stocks.items():
            this.deposit += get_last_price(ticker) * shares
            if ticker in this.portfolio:
                this.portfolio[ticker] += shares
            else:
                this.portfolio[ticker] = shares

portfolio = {'MSFT':1, 'AAPL':5}
sim = Simulation(portfolio)
