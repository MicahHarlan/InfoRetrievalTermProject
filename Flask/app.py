from flask import Flask, render_template,jsonify,request
import llm
generator = llm.init_generator()

app = Flask(__name__)

#@app.route('/user_input',methods=['POST'])
#def user_query():
#	query = request.form.get('search-input', 'Default Value')	
#	print(f'Query: {query}')
#	return 'Ello'

@app.route('/getLLMResponse',methods=['POST'])
def llm_response():
	data = request.get_json()
	user_input = data.get('userInput')
    # Process the input and generate a response
	response_message = llm.get_llm(user_input,generator)
	return jsonify({'message': response_message})

@app.route('/')
def home():
	return render_template('index.html')

if __name__ == '__main__':
	app.run()

