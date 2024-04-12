from transformers import pipeline, set_seed


'''
The tokenizer or generators should run in this function and set to a var
in the flask app, so it only runs once.
'''
def init_generator():
	generator = pipeline('text-generation', model='gpt2')
	return generator

'''
Make sure this returns a string.
'''
def get_llm(prompt,generator):
	responses = generator(prompt, max_length=50, num_return_sequences=1)
	return responses[0]['generated_text'] 
	# Generate


