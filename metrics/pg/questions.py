import os
import json

import pandas as pd
import predictionguard as pg
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator
from tqdm import tqdm


def load_token():
    with open("../../config/predictionguard.json", 'r') as file:
        config = json.load(file)
        return config['api_key']


class Prompt(BaseModel):
    prompt: str = Field(
        ...,
        title="Prompt",
        description="The prompt to be used for generating the completion.",
    )


os.environ["PREDICTIONGUARD_TOKEN"] = load_token()

parser = PydanticOutputParser(pydantic_object=Prompt)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

tag_movies = pd.read_csv('../tag_movies.csv')
tag_movies = tag_movies[tag_movies['tag'].notna()]
tag_movies['tag'] = tag_movies['tag'].str.lower()
for index, row in tag_movies.iterrows():
    print(row['tag'], row['title'])

# prompt_expecte
for index, row in tqdm(tag_movies.iterrows()):
    result = pg.Completion.create(
        model="Neural-Chat-7B",
        prompt=prompt.format(query="Generate a question to ask about movies related to this tag: " + row['tag']),
        max_tokens=200,
        temperature=0.1
    )
    try:
        question = Prompt.parse_raw(result['choices'][0]['text'])
        with open('results.csv', 'a') as f:
            f.write(f"{row['tag']},{question.prompt}\n")
    except Exception as e:
        print(f"Error parsing: {e}")

# result = pg.Completion.create(
#     model="Neural-Chat-7B",
#     prompt=prompt.format(query="Generate a question to ask about movie related to this tag: " + "spoof"),
#     max_tokens=200,
#     temperature=0.1
# )
# try:
#     questions = Prompt.parse_raw(result['choices'][0]['text'])
#     print(f"Prompt: {questions.prompt}")
# except Exception as e:
#     print(f"Error parsing joke: {e}")
