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
	responses = [send_to_fastapi(name) for name in titles]
	movies= []
	for r in responses:
		image_url = f"https://image.tmdb.org/t/p/w185{r[0]['image']}"
		movie = {'title':r[0]['primaryTitle'],'director':r[0]['directors'],'image':image_url}
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

if __name__ == '__main__':
	#For running on local host.
	app.run(debug=True)
	#To run on so people connected to wifi can connect.
	#flask run on command line
	#app.run(host='0.0.0.0', port=5000)	
