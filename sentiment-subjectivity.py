import sqlite3
import statistics
from collections import defaultdict
import matplotlib.pyplot as plt

import tqdm
from textblob import TextBlob

database = sqlite3.connect('hj/hj_activity.db')
cursor = database.cursor()
cursor.execute('''SELECT Messages.author_id, Messages.content FROM Messages WHERE channel_id='152536219933212673';''')

polarity = defaultdict(lambda: [])
subjectivity = defaultdict(lambda: [])

polarity_averages = {}
subjectivity_averages = {}

results = cursor.fetchall()
with tqdm.tqdm(total=len(results)) as p:
    for t in results:
        txt = TextBlob(t[1])
        polarity[t[0]].append(txt.sentiment.polarity)
        subjectivity[t[0]].append(txt.sentiment.subjectivity)
        p.update(1)

with tqdm.tqdm(total=len(polarity)) as p:
    for author, pols in polarity.items():
        polarity_averages[author] = statistics.mean(pols)
        p.update(1)

with tqdm.tqdm(total=len(subjectivity)) as p:
    for author, subs in subjectivity.items():
        subjectivity_averages[author] = statistics.mean(subs)
        p.update(1)

combined = defaultdict(list)
for d in (polarity_averages, subjectivity_averages):
    for k, v in d.items():
        combined[k].append(v)

combined = {k: v for k, v in combined.items() if v[0] != 0 and v[1] != 0}
combined = [[v[0], v[1]] for k, v in combined.items()]

plt.scatter([x[0] for x in combined], [x[1] for x in combined], s=2)  # x axis is polarity, y axis is subjectivity
plt.xlim(-1, 1)
plt.ylim(0, 1)
plt.title("Polarity-subjectivity plot of users in XXXX")
plt.xlabel("Polarity")
plt.ylabel("Subjectivity")
plt.grid(which='major', linewidth=0.5)
plt.grid(which='minor', linewidth=0.2)
plt.savefig('hj_sentiment_subjectivity.png', dpi=500)
plt.clf()

plt.scatter([x[0] for x in combined], [x[1] for x in combined], s=2)  # x axis is polarity, y axis is subjectivity
plt.title("Polarity-subjectivity plot of users in XXXX")
plt.xlabel("Polarity")
plt.ylabel("Subjectivity")
plt.grid(which='major', linewidth=0.5)
plt.grid(which='minor', linewidth=0.2)
plt.savefig('hj_sentiment_subjectivity_scaled.png', dpi=500)

