import sqlite3
import statistics
from textblob import TextBlob

database = sqlite3.connect('hj/hj_activity.db')
cursor = database.cursor()
cursor.execute('''SELECT Messages.content FROM Messages WHERE channel_id='610233358185791530';''')
content = [TextBlob(x[0]).sentiment.polarity for x in cursor.fetchall()]
average = statistics.mean(content)
print(f'#star average polarity - {average}')
