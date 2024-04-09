import sqlite3
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

"Do something to create table if needed"



count = 0
cursor.execute('''

SELECT * 
FROM Movie 

''')

for row in cursor.fetchall():
    imdb_id = row[0]  # 'tt0003854'

    find = tmdb.Find(imdb_id)
    find.info(external_source='imdb_id')
    if find.movie_results:
        plot = find.movie_results[0].get('overview', '')
        image = find.movie_results[0].get('poster_path', '')
        # Update the movie record with new plot and image path
        cursor.execute('''
            UPDATE Movie
            SET plot = ?, image = ?
            WHERE MovieID = ?
            ''', (plot, image, imdb_id))
        conn.commit()  # Commit changes to the database
        count += 1

print(count)

conn.close()
