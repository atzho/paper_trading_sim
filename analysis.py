from simulation import *

def compare(portfolios, start, end):
    sims = [Simulation(portfolio, date=start) for portfolio in portfolios]

    for sim in sims:
        sim.date = end

    return [{'portfolio':sim.portfolio,
             'initial_value':-sim.balance,
             'end_value':sim.value(),
             'gains':sim.gains(),
             'percent_change':sim.value()/(-sim.balance) * 100} for sim in sims]
