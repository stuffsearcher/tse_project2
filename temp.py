import pandas
import matplotlib.pyplot as plt

f = pandas.read_csv("cwd/data.csv")

f.columns = ["Date", "Speed", "Direction"]

y = pandas.cut(f["Speed"], [0, 2, 4, 6, 8, 10, 12, 14])

f["bins"] = y

# f = f.set_index("Date")  or f.set_index('Time', inplace=True)
f["Date"] = pandas.to_datetime(f["Date"])
filt = f["Date"].dt.hour == 4
f.set_index("Date")["Speed"].resample("D").mean().count()
f.groupby("bins").mean()["Speed"]
plt.hlines(f["Speed"].mean(), 0, len(f))
plt.plot(range(len(f)), f["Speed"])
plt.show()
