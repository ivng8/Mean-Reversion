import requests
import csv
import numpy as np
import scipy.stats as stats

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

dates = data['Time Series (Daily)'].keys()
Foo = []

for date in dates:
    Foo.append([date, 'IBM', float(data['Time Series (Daily)'][date]['5. adjusted close'])])

Foo = Foo[:100]
Foo.reverse()

for i in range(1, 100):
    Foo[i].append(np.log(Foo[i][2]) - np.log(Foo[i-1][2]))

def export(fileName, data):
    with open(fileName, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

def ma_app(maN):
    FooN = Foo.copy()

    ma = []
    for i in range(100):
        ma.append(FooN[i][2])
        if i > maN - 1:
            ma.pop(0)
        if i > maN - 2:
            FooN[i].append(np.mean(ma))
    
    return FooN

def buy_tick(data, maN, k):
    for i in range(maN, 100):
        if data[i][2] - data[i-1][4] > k:
            data[i].append(1)
        else:
            data[i].append(0)

    for i in range(maN + 1, 100):
        if data[i-1][5] == 1:
            data[i].append(data[i][3])
        else:
            data[i].append(0)

def return_p(data, maN):
    returns = 1
    for i in range(maN + 1, 100):
        returns *= (data[i][6] + 1)
    annualized_return = returns ** 3.65
    return returns - 1, annualized_return - 1

def t_test(data, maN):
    daily_p_returns = []
    for i in range(maN + 1, 100):
        if data[i][6] != 0:
            daily_p_returns.append(data[i][6])

    t_stat, p_value = stats.ttest_1samp(daily_p_returns, 0)
    print("T-stat:", t_stat)
    print("P-value:", p_value)

export("Base.csv", Foo)

Foo3 = ma_app(3)
buy_tick(Foo3, 3, 0.0)
export("3_Day.csv", Foo3)
returns, annualized_return = return_p(Foo3, 3)
print("3 Day Moving Average", returns, "Annualized Return:", annualized_return)
t_test(Foo3, 3)

Foo5 = ma_app(5)
buy_tick(Foo5, 5, 0.0)
export("5_Day.csv", Foo5)
returns, annualized_return = return_p(Foo5, 5)
print("5 Day Moving Average", returns, "Annualized Return:", annualized_return)
t_test(Foo5, 5)

