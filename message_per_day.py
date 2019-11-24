import datetime
import tqdm as tq
from matplotlib import pyplot as plt
import matplotlib.dates as mpldates
import numpy as np
import sqlite3
from matplotlib.ticker import FuncFormatter


def m_fmt(x, pos=None):
    return month_fmt(x)[0]


database = sqlite3.connect('hj/hj_activity.db')

cursor = database.cursor()
cursor.execute('''SELECT timestamp FROM Messages ORDER BY timestamp ASC''')
timestamps = [datetime.date.fromtimestamp(x[0]) for x in cursor.fetchall()]
counts = [[x, timestamps.count(x)] for x in set(timestamps)]
aggregate = np.asarray(counts)
aggregate = aggregate[aggregate[:, 0].argsort()]

years = mpldates.YearLocator()
months = mpldates.MonthLocator()
month_fmt = mpldates.DateFormatter('%b')

x_axis = mpldates.DateFormatter('%Y')

fig, ax = plt.subplots()
ax.plot(aggregate[:, 0], aggregate[:, 1], linewidth=0.5)
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(mpldates.DateFormatter('%Y'))
ax.xaxis.set_minor_locator(months)
# ax.xaxis.set_minor_formatter(mpldates.DateFormatter('%B'))
ax.xaxis.set_minor_formatter(FuncFormatter(m_fmt), )
ax.format_xdata = mpldates.DateFormatter('%Y-%m-%d')
ax.grid(True)
fig.autofmt_xdate()
ax.tick_params(axis='both', which='minor', labelsize=4)
plt.title("Messages per day over guild lifetime")
plt.xlabel("Date")
plt.ylabel("Messages per day")
plt.savefig('hj_messages_per_day.png', dpi=500)

# with tq.tqdm(leave=True, unit=' messages', total=len(results)) as counter:
