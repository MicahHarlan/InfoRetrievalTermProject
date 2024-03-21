movie_titles = ['The Shawshank Redemption', 'Saw', 'The Godfather', 'The Dark Knight']

for title in movie_titles:
    input_texts = f"<s>[INST] Write a description of the movie '{title}.' [/INST]"
    input_ids = tokenizer(input_texts, return_tensors="pt")
    outputs = model.generate(**input_ids, generation_config=generation_config)
    print(tokenizer.batch_decode(outputs, skip_special_tokens=True))