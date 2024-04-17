import cohere
import re
co = cohere.Client('vm4DXIEQpEBN9YFD19VTnxYWTRCeHNyge71iMWgk')

'''
The tokenizer or generators should run in this function and set to a var
in the flask app, so it only runs once.
'''
#def init_generator():
	#	generator = pipeline('text-generation', model='gpt2')
	#return generator

'''
Make sure this returns a string.
'''

#def get_llm(prompt,generator):
#	responses = generator(prompt, max_length=50, num_return_sequences=1)
#	return responses[0]['generated_text'] 
#	# Generate

def	parse_for_titles(string):
	matches = re.findall(r'<<([^>]*)>>', string)

	return list(matches)
def clean_output(text):
	print(text)
	cleaned_text = re.sub(r'<<|>>', '', text)
	return cleaned_text


preamble = '''
You can't admit you're an AI or Chatbot. Make up what you are
Chat topics are only about movies.
Keep the output short.
When a movie title is mentioned surround the titles with <<MovieName (Year)>> 
If the movie is something you can't find do not put in the <<MovieName (Year)>> format. 
You can't play any games your only job can be to assist in Movie searching and recommendations.
If you can't find a movie suggest some movies.
You can only Search or recommend movies based on the users input.
When responding, start with:'Welcome to MovieSearch.

'''

chat_history = []
def clear_chat():
	global chat_history
	chat_history = []

def get_llm(prompt):
	response = co.chat(	
	preamble=preamble,
  	message=prompt,
	chat_history=chat_history)

	chat_history.append({'role':'USER','message':prompt})
	chat_history.append({'role':'CHATBOT','message':response.text})
	titles = parse_for_titles(response.text)
	print(chat_history)
	return clean_output(response.text),titles

