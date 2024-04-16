import json

import requests
from flask import Flask, render_template,jsonify,request
import llm

app = Flask(__name__)
@app.route('/getLLMResponse',methods=['POST'])
def llm_response():
	'''This function deals with useer input and LLM output.'''
	data = request.get_json()
	user_input = data.get('userInput')
    # Process the input and generate a response
	response_message,titles = llm.get_llm(user_input)
	responses = get_list_of_movies_by_titles(titles)   #[send_to_fastapi(name) for name in titles]
	movies= []
	for r in responses:
		image_url = f"https://image.tmdb.org/t/p/w185{r['image']}"
		movie = {'title':r['primaryTitle'],'director':r['directors'],'image':image_url}
		print(movie)
		movies.append(movie)
	clean_movies = [movie if isinstance(movie, dict) else movie.__dict__ for movie in movies]
		

	return jsonify({'message': response_message,'titles':clean_movies})

@app.route('/')
def home():
	return render_template('index.html')

def send_to_fastapi(query):	
	print(query)
	url = 'http://127.0.0.1:8000/search'
	params = {'q': query}
	response = requests.get(url, params=params)
	return response.json()

def get_list_of_movies_by_titles(titles):
	url = 'http://127.0.0.1:8000/listofmovies/'
	titles = ['Forrest Gump', 'The Matrix', 'The Godfather']
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
