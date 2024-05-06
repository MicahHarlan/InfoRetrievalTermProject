import sqlite3

import pandas as pd
import tmdbsimple as tmdb
import json

def load_api_key():
    with open("../config/tmdb.json", 'r') as file:
        config = json.load(file)
        return config['api_key']

tmdb.API_KEY = load_api_key()

# Connect to SQLite database (or create it)
conn = sqlite3.connect('../fastapi/query/movie.db')
cursor = conn.cursor()

# Create tables if needed
# Example: cursor.execute("CREATE TABLE IF NOT EXISTS Movie (column1 TYPE, column2 TYPE)")

# Query movies
cursor.execute('''
    SELECT * 
    FROM Movie 
''')

beginning_director_id = 1
count = 0

data = []

for row in cursor.fetchall():
    count += 1
    if count % 100 == 0:
        print(count)
    imdb_id = row[0]  # 'tt0003854'

    find = tmdb.Find(imdb_id)
    find.info(external_source='imdb_id')
    if find.movie_results:
        movie_id = find.movie_results[0].get('id', '')
        if movie_id:
            movie_credit = tmdb.Movies(movie_id).credits()
            director = ''
            for credit in movie_credit['crew']:
                if credit['job'] == 'Director':
                    director = credit['name']
                    break
            print(director)
            # Append dictionary to the list instead of DataFrame
            data.append({'MovieID': imdb_id, 'Director': director})
        else:
            continue

df = pd.DataFrame(data)
df.to_csv('directors.csv', index=False)

# Close the connection
conn.close()

print(count)
