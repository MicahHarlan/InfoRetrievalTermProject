import pandas as pd
import sqlite3
import tmdbsimple as tmdb

# Connect to SQLite database (or create it)
conn = sqlite3.connect('../fastapi/query/movie.db')
cursor = conn.cursor()

count = 0
cursor.execute('''

SELECT * 
FROM Movie 

''')

df = pd.read_sql_query('''
SELECT *
FROM Movie
''', conn)

df.to_csv('movies.csv', index=False)
