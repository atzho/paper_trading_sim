import yfinance as yf
import pandas as pd
import json

# Author: Andrew Zhong

def get_last_price(ticker):
    return yf.Ticker(ticker).history().tail(1)['Close'].iloc[0]

def get_price_at(ticker, date):
    tmr_ts = pd.Timestamp(date) + pd.to_timedelta(1, unit='d')
    tomorrow = '%i-%i-%i' % (tmr_ts.year, tmr_ts.month, tmr_ts.day)

    try:
        return get_historical_data([ticker], date, tomorrow)[ticker].Open[0]
    except:
        raise Exception('No data found for date %s' % date)

# start and end in "YEAR-MO-DA" format, with 0s in front
def get_historical_data(tickers, start, end):
    if len(tickers) == 0:
        raise Exception('No tickers provided')
    data = yf.download(tickers, start=start,
                       end=end, group_by='tickers')
    if len(data.columns) == 6:
        series = {tickers[0] : data}
    else:
        series = {ticker : data[ticker]['Open'] for ticker in tickers}
    return series

class Simulation:

    # name, portfolio, date, balance
    def __init__(this, portfolio, name=None, date=None, balance=None, deposits=0):
        this.portfolio = portfolio
        this.name = name
        this.deposits = deposits
        if date:
            this.date = date
        else:
            today = pd.Timestamp.today()
            this.date = '%i-%i-%i' % (today.year, today.month, today.day)
        if balance:
            this.balance = balance
        else:
            this.balance = -this.value()

    def update_date(this):
        today = pd.Timestamp.today()
        this.date = '%i-%i-%i' % (today.year, today.month, today.day)

    # Value calculations
    def value(this):
        return sum([shares * get_price_at(ticker, this.date) for ticker, shares in this.portfolio.items()])

    def gains(this):
        return this.balance + this.value() - this.deposits

    def present_value(this):
        return sum([shares * get_last_price(ticker) for ticker, shares in this.portfolio.items()])

    def present_gains(this):
        return this.balance + this.present_value() - this.deposits

    # Actions
    def deposit(this, amount):
        this.balance += amount
        this.deposits += amount
        this.log('Deposited %f. Balance: %f' % (amount, this.balance))
    
    def buy(this, stocks):
        for ticker, shares in stocks.items():
            this.balance -= get_price_at(ticker, this.date) * shares
            if ticker in this.portfolio:
                this.portfolio[ticker] += shares
            else:
                this.portfolio[ticker] = shares
                
        this.save_to_json()
        this.log('Bought %s on %s. Balance: %f. Portfolio value: %f'
                      % (repr(stocks), this.date, this.balance, this.value()))
                         
    def sell(this, stocks):
        for ticker, shares in stocks.items():
            this.balance += get_price_at(ticker, this.date) * shares
            if ticker in this.portfolio:
                this.portfolio[ticker] -= shares
            else:
                this.portfolio[ticker] = shares
                
        this.save_to_json()
        this.log('Sold %s on %s. Balance: %f. Portfolio value: %f'
                      % (repr(stocks), this.date, this.balance, this.value()))

    # File Interactions
    @classmethod
    def load_json(cls, filepath):
        data = json.load(open(filepath))
        return cls(data['name'],
                   data['portfolio'],
                   data['date'],
                   data['balance'],
                   data['deposits'])

    def save_to_json(this):
        with open(this.name + '.json', 'w') as file:
            save = json.dump({'name': this.name,
                              'date': this.date,
                              'portfolio' : this.portfolio,
                              'balance': this.balance,
                              'deposits': this.deposits},
                             file)
    def log(this, msg):
        open(this.name + '.log', 'a').write(msg + '\n')

##if __name__ == "__main__":
##    sim = Simulation.load_json('test_sim.json')
        
