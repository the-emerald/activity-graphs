import re
import sqlite3
from wordcloud import WordCloud, STOPWORDS
import nltk

database = sqlite3.connect('hj/hj_activity.db')

cursor = database.cursor()
cursor.execute('''SELECT content FROM Messages WHERE author_id='99820161594294272';''')
content = [x[0] for x in cursor.fetchall()]

# No URLs
content = [re.sub(r'(?:(?:http|https):\/\/)?([-a-zA-Z0-9.]{2,256}\.[a-z]{2,4})\b(?:\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?',
                  "", c, flags=re.MULTILINE) for c in content]

content = [nltk.word_tokenize(x.lower()) for x in content]
content = [item for sublist in content for item in sublist]

stopwords = set(STOPWORDS)
stopwords.update([x for x in content if len(x.strip()) <= 3])
# stopwords.update(["n't"])

word_cloud = WordCloud(stopwords=stopwords, max_font_size=500, max_words=100, background_color="white", width=4000,
                       height=2000).generate(' '.join([elem for elem in content]))
word_cloud.to_file("hj_emerald_wordcloud.png")
