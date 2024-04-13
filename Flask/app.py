import requests
from flask import Flask, render_template,jsonify,request
import llm
#generator = llm.init_generator()

app = Flask(__name__)

@app.route('/getLLMResponse',methods=['POST'])
def llm_response():
	'''This function deals with useer input and LLM output.'''
	data = request.get_json()
	user_input = data.get('userInput')
    # Process the input and generate a response
	response_message,titles = llm.get_llm(user_input)

	# Testing fastapi output
	print(send_to_fastapi("Forrest Gump"))
	
	return jsonify({'message': response_message,'titles':titles})

@app.route('/')
def home():
	return render_template('index.html')

def send_to_fastapi(query):
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
