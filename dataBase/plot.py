import sqlite3
import tmdbsimple as tmdb
import json

def load_api_key():
    with open("../config/tmdb.json", 'r') as file:
        config = json.load(file)
        return config['api_key']

tmdb.API_KEY = load_api_key()



# Connect to SQLite database (or create it)
connection = sqlite3.connect('movie.db')
cursor = connection.cursor()

"Do something to create table if needed"

count = 0
cursor.execute('''

SELECT * 
FROM Movie 
WHERE Year > 1990 AND runtimeMinutes > 90 AND avgRating > 3.5
ORDER BY Year DESC 
LIMIT 10

''')

for row in cursor.fetchall():
    imdb_id = row[0]  # 'tt0003854'
    title = row[1]  # 'Dodge City Trail'
    year = row[2]  # 1936
    movie_title = row[3]  # 'Dodge City Trail'
    duration = row[4]  # 56 (minutes)
    rating = row[5]  # 3.7

    find = tmdb.Find(imdb_id)
    find.info(external_source='imdb_id')
    print(row)
    print(find.movie_results[0]['overview'])
    count += 1

print(count)

connection.close()
