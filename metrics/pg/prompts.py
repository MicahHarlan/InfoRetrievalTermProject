import os
import json
import predictionguard as pg

def load_token():
    with open("../../config/predictionguard.json", 'r') as file:
        config = json.load(file)
        return config['api_key']

os.environ["PREDICTIONGUARD_TOKEN"] = load_token()

# Define our prompt.

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. Your model is hosted by Prediction Guard, a leading AI company."
    },
    {
        "role": "user",
        "content": "Where can I access the LLMs in a safe and secure environment?"
    }
]

# result = pg.Chat.create(
#     model="Neural-Chat-7B",
#     messages=messages
# )

result = pg.Completion.create(
    model="Nous-Hermes-Llama2-13B",
    prompt="""### Instruction:
Summarize the following movies in the input section. 
Use a sentence for each movie that includes information of title and plot. 
Start response with 'Welcome to IR24 Movie Group LLM Demo'
### Input:
[
  {
    "primaryTitle": "Steve Jobs",
    "plot": "Set backstage at three iconic product launches and ending in 1998 with the unveiling of the iMac, Steve Jobs takes us behind the scenes of the digital revolution to paint an intimate portrait of the brilliant man at its epicenter.",
  },
  {
    "primaryTitle": "Jobs",
    "plot": "The story of Steve Jobs' ascension from college dropout into one of the most revered creative entrepreneurs of the 20th century.",
  }]
### Response:
"""
)

print(json.dumps(
    result,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
))
