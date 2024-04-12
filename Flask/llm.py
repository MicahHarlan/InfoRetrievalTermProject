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
	return list(set(matches))
def clean_output(text):
	cleaned_text = re.sub(r'<<|>>', '', text)
	return cleaned_text


preamble = '''Topics are only about movies.
Keep the output short.
When a movie title is mentioned surround the titles with <<MovieName>> 
If the movie is something you can't find do not put in the <<MovieName>> format. 
When responing start with:'Welcome to MovieSearch.'''

def get_llm(prompt):
	response = co.chat(	
	preamble=preamble,
  	message=prompt
	)
	titles = parse_for_titles(response.text)
	print(titles)
	return clean_output(response.text),titles

