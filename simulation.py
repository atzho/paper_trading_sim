import yfinance as yf

def get_last_price(ticker):
    return yf.Ticker(ticker).history().tail(1)['Close'].iloc[0]

class Simulation:

    def __init__(this, portfolio):
        this.portfolio = portfolio
        this.deposit = this.calc_value()

    def calc_value(this):
        return sum([shares * get_last_price(ticker) for ticker, shares in this.portfolio.items()])

    def calc_gains(this):
        return this.deposit - this.calc_value()

    def buy_stocks(this, stocks):
        for ticker, shares in stocks.items():
            this.deposit += get_last_price(ticker) * shares
            if ticker in this.portfolio:
                this.portfolio[ticker] += shares
            else:
                this.portfolio[ticker] = shares

portfolio = {'MSFT':1, 'AAPL':5}
sim = Simulation(portfolio)
