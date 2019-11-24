import datetime
import statistics
from collections import defaultdict

import tqdm
import tqdm as tq
from matplotlib import pyplot as plt
import matplotlib.dates as mpldates
import numpy as np
import sqlite3
from matplotlib.ticker import FuncFormatter
from textblob import TextBlob

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def m_fmt(x, pos=None):
    return month_fmt(x)[0]


database = sqlite3.connect('hj/hj_activity.db')
sentiment_db = sqlite3.connect('hj/emerald_sentiment.db')

sentiment_cursor = sentiment_db.cursor()
sentiment_cursor.execute('''DROP TABLE IF EXISTS Sentiments''')
sentiment_cursor.execute('''CREATE TABLE IF NOT EXISTS Sentiments (message_id INT NOT NULL, sentiment REAL NOT NULL, 
timestamp INT NOT NULL)''')

sentiment_db.commit()


cursor = database.cursor()
cursor.execute('''SELECT message_id, content, timestamp FROM Messages WHERE Messages.author_id = '99820161594294272'
 ORDER BY timestamp ASC''')

contents = [[x[0], TextBlob(x[1]), x[2]] for x in cursor.fetchall()]
with tqdm.tqdm(total=len(contents)) as p:
    for c in contents:
        c[1] = c[1].sentiment.polarity
        p.update(1)

contents = [c for c in contents if c[1] != 0]
sentiment_cursor.executemany('''INSERT INTO Sentiments VALUES (?, ?, ?)''', [(int(x[0]), float(x[1]), int(x[2])) for x in contents])
sentiment_db.commit()

timestamps = []
sentiments = []

sentiment_cursor.execute('''SELECT AVG(sentiment), timestamp FROM Sentiments GROUP BY date(timestamp, 'unixepoch')
 ORDER BY timestamp ASC''')
for x in sentiment_cursor.fetchall():
    timestamps.append(datetime.date.fromtimestamp(x[1]))
    sentiments.append(x[0])

# contents = []
# contents = list(map(list, zip([(date, map(map(filter(contents, lambda b: b[0]==date), lambda a: a[1]),
#                                           lambda c: sum(c)/len(c))) for date, _ in contents])))

years = mpldates.YearLocator()
months = mpldates.MonthLocator()
month_fmt = mpldates.DateFormatter('%b')

x_axis = mpldates.DateFormatter('%Y')

fig, ax = plt.subplots()
ax.plot(timestamps, sentiments, linewidth=0.5)
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(mpldates.DateFormatter('%Y'))
ax.xaxis.set_minor_locator(months)
# ax.xaxis.set_minor_formatter(mpldates.DateFormatter('%B'))
ax.xaxis.set_minor_formatter(FuncFormatter(m_fmt), )
ax.format_xdata = mpldates.DateFormatter('%Y-%m-%d')
ax.grid(True)
fig.autofmt_xdate()
ax.tick_params(axis='both', which='minor', labelsize=4)
plt.title("Sentiment per day of @XXXX")
plt.xlabel("Date")
plt.ylabel("Average sentiment")
plt.savefig('emerald_sentiment_per_day.png', dpi=500)

# with tq.tqdm(leave=True, unit=' messages', total=len(results)) as counter:
