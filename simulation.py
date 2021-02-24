import yfinance as yf
import pandas as pd
import json

def get_last_price(ticker):
    return yf.Ticker(ticker).history().tail(1)['Close'].iloc[0]

def get_price_at(ticker, date):
    return yf.Ticker(ticker).history(date)['Open'][0]

# start and end in "YEAR-MO-DA" format, with 0s in front
def get_historical_data(tickers, start, end):
    data = yf.download(tickers, start=start,
                       end=end, group_by='tickers')

    series = {ticker : data[ticker]['Open'] for ticker in tickers}

class Simulation:

    # name, portfolio, date, balance
    def __init__(this, name, portfolio, date=None, balance=None):
        this.portfolio = portfolio
        this.name = name
        if date:
            this.date = date
        else:
            today = pd.Timestamp.today()
            this.date = '%i-%i-%i' % (today.year, today.month, today.day)
        if balance:
            this.balance = balance
        else:
            this.balance = -this.value()

    # Value calculations
    def value(this):
        return sum([shares * get_price_at(ticker, this.date) for ticker, shares in this.portfolio.items()])

    def gains(this):
        return this.balance + this.value()

    def present_value(this):
        return sum([shares * get_last_price(ticker) for ticker, shares in this.portfolio.items()])

    def present_gains(this):
        return this.balance + this.present_value()

    # Actions
    def deposit(this, amount):
        this.balance += amount
        this.log('Deposited %f. Balance: %f' % (amount, this.balance))
    
    def buy_stocks(this, stocks):
        for ticker, shares in stocks.items():
            this.balance -= get_price_at(ticker, this.date) * shares
            if ticker in this.portfolio:
                this.portfolio[ticker] += shares
            else:
                this.portfolio[ticker] = shares
                
        this.save_to_json()
        this.log('Bought %s on %s. Balance: %f. Portfolio value: %f'
                      % (repr(stocks), this.date, this.balance, this.value()))
                         
    def sell_stocks(this, stocks):
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
                   data['balance'])

    def save_to_json(this):
        with open(this.name + '.json', 'w') as file:
            save = json.dump({'name': this.name,
                              'date': this.date,
                              'portfolio' : this.portfolio,
                              'balance': this.balance},
                             file)
    def log(this, msg):
        open(this.name + '.log', 'a').write(msg + '\n')

sim = Simulation.load_json('test_sim.json')
