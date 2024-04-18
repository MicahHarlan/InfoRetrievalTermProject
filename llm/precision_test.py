import json
import re

import cohere
import pandas as pd
from tqdm import tqdm

from Flask.llm import get_llm
from Flask.llm import clear_chat

def check_format(text):
    pattern = r'^Welcome to MovieSearch[\s\S]*?\n- [^\n]+'
    return bool(re.match(pattern, text))

def load_token():
    with open("../config/cohere.json", 'r') as file:
        config = json.load(file)
        return config['api_key']

co = cohere.Client(load_token())

tests = pd.read_csv('/Users/baiyizhang/dev/PycharmProjects/cs5604/InfoRetrievalTermProject/llm/pg/tag_prompt_titles.csv')

llm_results = pd.DataFrame(columns=['Prompt', 'Actual', 'Expected', 'Precision', 'Recall', 'F1'])

llm_format_results = pd.DataFrame(columns=['Prompt', 'isResponseFormatted'])

iterations = 0

for index, row in tqdm(tests.iterrows()):
    iterations+= 1
    print((row['prompt']))
    p = row['prompt'].replace("\'", "")
    print(p)
    try:
        result_text, result_titles = get_llm(p)
    except Exception as e:
        print(e)
        continue
    expected_titles_str = re.sub(r'<<|>>', '', row['title'])
    expected_titles = expected_titles_str.split(" | ")
    true_positive = 0
    false_positive = 0
    false_negative = 0
    for title in result_titles:
        if title in expected_titles:
            true_positive += 1
        else:
            false_positive += 1
    for title in expected_titles:
        if title not in result_titles:
            false_negative += 1
    false_negative = min(12, false_negative)

    if true_positive + false_positive == 0:
        precision = 0
    else:
        precision = true_positive / (true_positive + false_positive)

    if true_positive + false_negative == 0:
        recall = 0
    else:
        recall = true_positive / (true_positive + false_negative)

    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1: {f1}")
    new_row = pd.DataFrame(
        {'Prompt': [row['prompt']], 'Actual': [len(result_titles)], 'Expected': [len(expected_titles)],
         'Precision': [precision], 'Recall': [recall], 'F1': [f1]})
    llm_results = pd.concat([llm_results, new_row], ignore_index=True)
    if check_format(result_text):
        is_formatted = 1
    llm_format_results = pd.concat([llm_format_results, pd.DataFrame({'Prompt': [row['prompt']], 'isResponseFormatted': [is_formatted]})], ignore_index=True)
    clear_chat()


llm_results.to_csv('llm_results.csv')
llm_format_results.to_csv('llm_format_results.csv')
