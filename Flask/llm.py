from transformers import pipeline, set_seed


#token = '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'
#generator = pipeline('text-generation', model='gpt2')

def init_generator():
	generator = pipeline('text-generation', model='gpt2')
	return generator
def get_llm(prompt,generator):
	responses = generator(prompt, max_length=50, num_return_sequences=1)
	return responses[0]['generated_text'] 
	# Generate


