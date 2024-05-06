import json
import requests
from flask import Flask, render_template, jsonify, request, redirect, url_for,session
import llm

from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

import tmdbsimple as tmdb

def load_api_key():
    with open("../config/tmdb.json", 'r') as file:
        config = json.load(file)
        return config['api_key']

tmdb.API_KEY = load_api_key()

app = Flask(__name__)

#Should be a super secret hard to guess
app.secret_key = '0000'

@app.route('/getLLMResponse',methods=['POST'])
def llm_response():
	'''This function deals with useer input and LLM output.'''

	data = request.get_json()
	user_input = data.get('userInput')
    # Process the input and generate a response
	response_message,titles = llm.get_llm(user_input)

	if titles:
		recs = get_recommendation_cluster(titles[0])
		for rec in recs:
			if rec not in titles:
				titles += recs

	responses = get_list_of_movies_by_titles(titles)   #[send_to_fastapi(name) for name in titles]
	movies= []
	#print(f'RESPONSS: {responses}')
	
	for r in responses:
		if type(r) == str:
			break	
		print(type(responses))
		if not r: 
			continue
		#print(f'r: {r}')
		image_url = f"https://image.tmdb.org/t/p/w185{r['image']}"
		#movie = {'title':r['primaryTitle'],'director':r['directors'],'image':image_url}
		movie = {'title':r['primaryTitle'],'image':image_url, 'directors':get_directors_by_imdbid(r['MovieID'])}
		
		movies.append(movie)
	clean_movies = [movie if isinstance(movie, dict) else movie.__dict__ for movie in movies]

	return jsonify({'message': response_message,'titles':clean_movies})

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/clear', methods=['POST'])
def clear_data():
	llm.clear_chat()
	return jsonify({'status': 'success', 'message': 'Data cleared successfully'})

import pandas as pd
df_cluster = pd.read_csv('../recommendation/movies_clustered.csv')

def get_recommendation_cluster(title):
	target_cluster = df_cluster[df_cluster['title'] == title].cluster
	movies_in_cluster = df_cluster[df_cluster['cluster'] == target_cluster.values[0]].title.tolist()
	# sort by numVotes * avgRating
	rec = []
	for movie in movies_in_cluster:
		rec.append((movie, df_cluster[df_cluster['title'] == movie].numVotes.values[0] * df_cluster[df_cluster['title'] == movie].avgRating.values[0]))
	rec = sorted(rec, key=lambda x: x[1], reverse=True)
	# Top 10:
	rec = [x[0] for x in rec[:10]]
	return rec

def get_recommendation_tfidf(title):
	tfidf = sparse.load_npz('../recommendation/tfidf_movieid.npz')
	cos_sim = cosine_similarity(tfidf, tfidf)
	indices = pd.Series(df_cluster.index, index=df_cluster['title']).drop_duplicates()
	recommended_movies = []
	index = indices[title]
	similarity_scores = pd.Series(cos_sim[index]).sort_values(ascending=False)
	top_10_movies = list(similarity_scores.iloc[1:11].index)
	for i in top_10_movies:
		recommended_movies.append(list(df_cluster['title'])[i])
	return recommended_movies


def get_movie_for_view(movie):
	title =  movie['primaryTitle']
	image_url = f"https://image.tmdb.org/t/p/w185{movie['image']}"
	year = movie['Year']
	plot = movie['plot']
	rating = movie['avgRating']
	genres = [g['genreName']for g in movie['genres']]
	directors = [d['Name']for d in movie['directors']]
	if not directors:
		directors = get_directors_by_imdbid(movie['MovieID'])
	actors = [a['Name'] for a in movie['actors'] ]

	return {'title': title, 'image':image_url,
			'year': year,'plot':plot,'rating':rating,
			'genres':genres,'actors':actors,'directors':directors}


def get_directors_by_imdbid(imdb_id):
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
			return [director]

@app.route('/view',methods=['POST'])
def view_movie():
	data = request.json
	movie = send_to_fastapi(data['title'])[0]
	#print(f'Movie: {movie}')
	image_url = f"https://image.tmdb.org/t/p/w185{movie['image']}"


	session['movie_info'] = get_movie_for_view(movie)
	return redirect(url_for('view_page'))

@app.route('/view')
def view_page():
	movie_info = session.get('movie_info', {})
	print(f'{movie_info}: movie_info')
	# Get the title from query parameters or set a default
	# Render your template with the title or perform other actions
	return render_template('view.html', movie=movie_info)


def send_to_fastapi(query):	
	url = 'http://127.0.0.1:8000/search'
	params = {'q': query}
	response = requests.get(url, params=params)
	return response.json()

def get_list_of_movies_by_titles(titles):
	url = 'http://127.0.0.1:8000/listofmovies/'
	headers = {'Content-Type': 'application/json'}  # Set header to application/json
	body = json.dumps(titles)  # Convert the list to a JSON formatted string

	try:
		response = requests.post(url, data=body, headers=headers)
		response.raise_for_status()  # Raises an HTTPError for bad responses
		return response.json()  # Return the JSON response
	except requests.exceptions.HTTPError as errh:
		return f"HTTP error occurred: {errh}"
	except requests.exceptions.ConnectionError as errc:
		return f"Error Connecting: {errc}"
	except requests.exceptions.Timeout as errt:
		return f"Timeout Error: {errt}"
	except requests.exceptions.RequestException as err:
		return f"An error occurred: {err}"

if __name__ == '__main__':
	#For running on local host.
	app.run(debug=True)
	#To run on so people connected to wifi can connect.
	#flask run on command line
	#app.run(host='0.0.0.0', port=5000)	


