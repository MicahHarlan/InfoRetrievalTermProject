import os
import json
# os.environ["LD_LIBRARY_PATH"] = "H:/conda_envs/langchain_env/libs"
# os.environ['HF_HOME'] = "H:/cache/hf_cache_home"
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

def load_token():
    with open("../config/huggingface.json", 'r') as file:
        config = json.load(file)
        return config['token']

token = load_token()

tokenizer = AutoTokenizer.from_pretrained("lmsys/vicuna-7b-v1.5", use_fast = False, token = token)
model = AutoModelForCausalLM.from_pretrained("lmsys/vicuna-7b-v1.5", token = token)
generation_config = GenerationConfig(
    max_new_tokens=500, do_sample=True, top_k=50, eos_token_id=model.config.eos_token_id
)


movie_titles = ['The Shawshank Redemption', 'Saw', 'The Godfather', 'The Dark Knight']

for title in movie_titles:
    input_texts = f"<s>[INST] Write a description of the movie '{title}.' [/INST]"
    input_ids = tokenizer(input_texts, return_tensors="pt")
    outputs = model.generate(**input_ids, generation_config=generation_config)
    print(tokenizer.batch_decode(outputs, skip_special_tokens=True))