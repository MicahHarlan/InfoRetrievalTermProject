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

# Create tables if needed
# Example: cursor.execute("CREATE TABLE IF NOT EXISTS Movie (column1 TYPE, column2 TYPE)")

# Query movies
cursor.execute('''
    SELECT * 
    FROM Movie 
''')

beginning_director_id = 1
count = 0

for row in cursor.fetchall():
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
            print(director, movie_credit, movie_id)
        else:
            continue

        # Find if Director ID exists
        cursor.execute('''
            SELECT DirectorID
            FROM Directors
            WHERE Name = ?
            ''', (director,))
        result = cursor.fetchone()
        if result:
            # Director exists
            dId = result[0]
        else:
            # Add director to Directors table
            dId = beginning_director_id
            beginning_director_id += 1
            cursor.execute('''
                INSERT INTO Directors (DirectorID, Name)
                VALUES (?, ?)
                ''', (dId, director))

        # Add entry to MovieDirectors table
        cursor.execute('''
            INSERT INTO MovieDirectors (MovieID, DirectorID)
            VALUES (?, ?)
            ''', (imdb_id, dId))

        conn.commit()  # Commit changes to the database
        count += 1

        # Close the cursor
        cursor.close()

# Close the connection
conn.close()

print(count)

# import sqlite3
# import tmdbsimple as tmdb
# import json
#
# def load_api_key():
#     with open("../config/tmdb.json", 'r') as file:
#         config = json.load(file)
#         return config['api_key']
#
# tmdb.API_KEY = load_api_key()
#
#
#
# # Connect to SQLite database (or create it)
# conn = sqlite3.connect('../fastapi/query/movie.db')
# cursor = conn.cursor()
#
# "Do something to create table if needed"
#
#
#
# count = 0
# cursor.execute('''
#
# SELECT *
# FROM Movie
#
# ''')
#
# beginning_director_id = 1
#
# for row in cursor.fetchall():
#     with sqlite3.connect('../fastapi/query/movie.db') as conn:
#         cursor = conn.cursor()
#         imdb_id = row[0]  # 'tt0003854'
#
#         find = tmdb.Find(imdb_id)
#         find.info(external_source='imdb_id')
#         if find.movie_results:
#             movie_id = find.movie_results[0].get('id', '')
#             if movie_id:
#                 movie_credit = tmdb.Movies(movie_id).credits()
#                 director = ''
#                 # response = movie.credits()
#                 # directors = [credit for credit in movie.crew if credit["job"] == "Director"]
#                 for credit in movie_credit['crew']:
#                     if credit['job'] == 'Director':
#                         director = credit['name']
#                         break
#                 print(director, movie_credit, movie_id)
#             else:
#                 continue
#
#             # Find if Director ID exists
#             cursor.execute('''
#                 SELECT DirectorID
#                 FROM Directors
#                 WHERE Name = ?
#                 ''', (director,))
#             result = cursor.fetchone()
#             if result:
#                 # Director exists
#                 dId = result[0]
#                 cursor.execute('''
#                     INSERT INTO MovieDirectors (MovieID, DirectorID)
#                     VALUES (?, ?)
#                     ''', (imdb_id, dId))
#             else:
#                 # add to Directors -> get Director ID
#                 # Maintain MovieDirectors table
#                 dId = beginning_director_id
#                 beginning_director_id += 1
#                 cursor.execute('''
#                     INSERT INTO Directors (DirectorID, Name)
#                     VALUES (?, ?)
#                     ''', (dId, director))
#                 cursor.execute('''
#                     INSERT INTO MovieDirectors (MovieID, DirectorID)
#                     VALUES (?, ?)
#                     ''', (imdb_id, dId))
#
#
#
#     conn.commit()
#     count += 1
#
# print(count)
#
# conn.close()
