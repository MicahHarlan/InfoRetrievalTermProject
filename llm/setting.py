import os
import json
os.environ['HF_Home'] = "resources"
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

