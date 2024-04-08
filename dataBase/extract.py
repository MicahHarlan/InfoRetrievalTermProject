import sqlite3
import pandas as pd


"""
make a smaller database with popular movies.
"""

database_path = '../fastapi/query/movie.db'


df = pd.read_csv('title.basics2.tsv',delimiter='\t',encoding='utf-8'
,low_memory=False)
df['startYear'] = pd.to_numeric(df['startYear'])
df = df[df['startYear'] >= 1930]
"Change year to int and remove older movies, < 1930"

print(df.head())

'df2 is the directors matrix with corresponding movie'
df2 = pd.read_csv('title.crew2.tsv',delimiter='\t',encoding='utf-8'
,low_memory=False)
df2 = df2[df2['tconst'].isin(df['tconst'])]

df3 = pd.read_csv('name.basics2.tsv',delimiter='\t',encoding='utf-8'
,low_memory=False)
df3 = df3[df3['knownForTitles'].isin(df['tconst'])]
df4 = pd.read_csv('title.ratings2.tsv',delimiter='\t',encoding='utf-8'
,low_memory=False)
df4 = df4[df4['tconst'].isin(df['tconst'])]

genres = df['genres'].str.split(',')
genres = genres.explode('genres')
genres = genres.unique()
movies = pd.merge(df, df4, on='tconst')


movie_genres = df[['tconst','genres']].copy()
movie_genres['genres'] = movie_genres['genres'].str.split(',')
movie_genres = movie_genres.explode('genres')

movies_popular = movies[movies['numVotes'] > 1000].copy()

movie_genres_popular = movie_genres[movie_genres['tconst'].isin(movies_popular['tconst'])].copy()

# movies_popular.to_csv('movies_popular.csv',index=False)

director_names = df3[df3['primaryProfession'] == 'director']
director_names_popular = director_names[director_names['knownForTitles'].isin(movies_popular['tconst'])].copy()
df3 = df3[df3['primaryProfession'] != 'director']
actors = df3[['nconst','primaryName']].copy()
actors.drop_duplicates(inplace=True)
actors.rename(columns={'nconst':'ActorID','primaryName':'Name'}
,inplace=True)

actor_movie = df3[['knownForTitles','nconst']].copy()
actor_movie.rename(columns={'nconst':'ActorID','knownForTitles':'MovieID'},inplace=True)

actor_movie_popular = actor_movie[actor_movie['MovieID'].isin(movies_popular['tconst'])].copy()
actors_popular = actors[actors['ActorID'].isin(actor_movie_popular['ActorID'])].copy()

# movies_popular.rename(columns={'tconst':'MovieID'},inplace=True)
# movies_popular.to_csv('movies_popular.csv',index=False)
# actor_movie_popular.to_csv('actor_movie_popular.csv',index=False)
# director_names_popular.to_csv('director_names_popular.csv',index=False)
# movie_genres_popular.to_csv('movie_genres_popular.csv',index=False)


"""
==============================
CREATING THE DATA BASE TABLES.
==============================
"""
'This file initializes the Movie Database.'
conn = sqlite3.connect('../fastapi/query/movie.db')
cursor = conn.cursor()
tables = ['genres','Movie','MovieGenres',
'Actors','Directors','MovieDirectors','MovieActors']

for t in tables:
	query = f'DROP TABLE IF EXISTS {t}'
	cursor.execute(query)


create_table_query = """
CREATE TABLE genres (
    genreName TEXT PRIMARY KEY
);
"""
cursor.execute(create_table_query)
for g in genres:
	cursor.execute("INSERT INTO genres (genreName) VALUES (?)",(g,))
del genres

cursor.execute("SELECT * FROM genres;")
row = cursor.fetchone()
print(row)


"""
====================
Creating Movie Table
====================
"""
create_table = """
CREATE TABLE IF NOT EXISTS Movie (
    MovieID VARCHAR(50) NOT NULL,
    primaryTitle VARCHAR(50),
    Year INTEGER, 
    originalTitle VARCHAR(50),
    runtimeMinutes INT,
    avgRating INT,
	numVotes INT,	
	plot TEXT,
	image VARCHAR(50),
    PRIMARY KEY (MovieID)
);
"""
cursor.execute(create_table)
for index, row in movies_popular.iterrows():
    cursor.execute("""
        INSERT INTO Movie (MovieID, primaryTitle, Year,originalTitle, runtimeMinutes, avgRating,numVotes, plot, image)
        VALUES (?,?, ?, ?, ?, ?, ?, "", "");""",
        (row['tconst'],
row['primaryTitle'],
 row['startYear'],row['originalTitle'],
row['runtimeMinutes'], row['averageRating'],row['numVotes']))

cursor.execute("SELECT primaryTitle FROM Movie WHERE Year=='1994';")
#row = cursor.fetchone()
#print(row)
create_table = """
CREATE TABLE IF NOT EXISTS MovieGenres (
	MovieID VARCHAR(50) NOT NULL, 
    genreName TEXT,
	PRIMARY KEY(MovieID,genreName),
	FOREIGN KEY (MovieID) REFERENCES Movie(MovieID),
	FOREIGN KEY (genreName) REFERENCES genres(genreName)
);
"""
cursor.execute(create_table)
movie_genres_popular.rename(columns={'tconst':'MovieID','genres':'genreName'}
, inplace=True)
movie_genres_popular.to_sql('MovieGenres', conn, if_exists='append', index=False)
cursor.execute("SELECT genreName FROM MovieGenres WHERE MovieID=='tt0003854' ")
print(cursor.fetchall())

create_table = """
CREATE TABLE IF NOT EXISTS Actors(
	ActorID VARCHAR(50) PRIMARY KEY,
	Name VARCHAR(50)
);
"""
cursor.execute(create_table)
actors_popular.to_sql('Actors', conn, if_exists='append', index=False)
cursor.execute("SELECT * FROM Actors;")
print(cursor.fetchone())

create_table = """ 
CREATE TABLE IF NOT EXISTS MovieActors (
    MovieID VARCHAR(50) NOT NULL, 
    ActorID VARCHAR(50),
   	PRIMARY KEY(MovieID,ActorID),
    FOREIGN KEY (MovieID) REFERENCES Movie(MovieID),
    FOREIGN KEY (ActorID) REFERENCES Actors(ActorID)
);
"""
cursor.execute(create_table)
actor_movie_popular.to_sql('MovieActors', conn, if_exists='append', index=False)
cursor.execute("SELECT * FROM MovieActors;")
print(cursor.fetchone())

directors_tab = director_names_popular[['nconst','primaryName']].copy()
directors_tab.drop_duplicates(inplace=True)
directors_tab.rename(columns={'nconst':'DirectorID', 'primaryName':'Name'},
inplace=True)

df2['directors'] = df2['directors'].str.split(',')
df2 = df2.explode('directors')
df2 = df2[df2['directors'].isin(directors_tab['DirectorID'])]
director_names_popular = df2[['tconst','directors']]
director_names_popular.rename(columns={'tconst':'MovieID',
'directors':'DirectorID'},inplace=True)




create_table = """
CREATE TABLE IF NOT EXISTS Directors(
	DirectorID VARCHAR(50) PRIMARY KEY,
	Name VARCHAR(50)
);
"""
cursor.execute(create_table)


directors_tab.to_sql('Directors', conn, if_exists='append', index=False)
cursor.execute("SELECT * FROM Directors;")
print(cursor.fetchone())


create_table = """ 
CREATE TABLE IF NOT EXISTS MovieDirectors(
    MovieID VARCHAR(50) NOT NULL, 
    DirectorID VARCHAR(50),
   	PRIMARY KEY(MovieID,DirectorID),
df2['directors'] = df2['directors'].str.split(',')    FOREIGN KEY (MovieID) REFERENCES Movie(MovieID),
    FOREIGN KEY (DirectorID) REFERENCES Directors(DirectorID)
);
"""
director_names_popular.to_sql('MovieDirectors', conn,
if_exists='append', index=False)
cursor.execute("SELECT * FROM MovieDirectors;")
print(cursor.fetchone())
conn.commit()
#Always add conn.close to the end
conn.close()

