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

ma = []
for i in range(100):
    ma.append(Foo[i][2])
    if i > 2:
        ma.pop(0)
    if i > 1:
        Foo[i].append(np.mean(ma))
    
for i in range(3, 100):
    if Foo[i][2] > Foo[i-1][4]:
        Foo[i].append(1)
    else:
        Foo[i].append(0)

for i in range(4, 100):
    if Foo[i-1][5] == 1:
        Foo[i].append(Foo[i][3])
    else:
        Foo[i].append(0)

with open("3_Day.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(Foo)

returns = 1
for i in range(4, 100):
    returns *= (Foo[i][6] + 1)

annualized_return = returns ** 3.65

print("3 Day Moving Average", returns - 1, "Annualized Return:", annualized_return - 1)

daily_p_returns = []
for i in range(4, 100):
    if Foo[i][6] != 0:
        daily_p_returns.append(Foo[i][6])

t_stat, p_value = stats.ttest_1samp(daily_p_returns, 0)
print("T-stat:", t_stat)
print("P-value:", p_value)

ma = []
for i in range(100):
    ma.append(Foo[i][2])
    if i > 4:
        ma.pop(0)
    if i > 3:
        Foo[i].append(np.mean(ma))
    
for i in range(5, 100):
    if Foo[i][2] > Foo[i-1][7]:
        Foo[i].append(1)
    else:
        Foo[i].append(0)

for i in range(6, 100):
    if Foo[i-1][8] == 1:
        Foo[i].append(Foo[i][3])
    else:
        Foo[i].append(0)

with open("5_Day.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(Foo)

returns = 1
for i in range(6, 100):
    returns *= (Foo[i][9] + 1)

annualized_return = returns ** 3.65

print("5 Day Moving Average", returns - 1, "Annualized Return:", annualized_return - 1)