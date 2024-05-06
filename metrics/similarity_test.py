import json
import re

import cohere
import pandas as pd
from tqdm import tqdm

from Flask.llm import get_llm
from Flask.llm import clear_chat


def load_token():
    with open("../config/cohere.json", 'r') as file:
        config = json.load(file)
        return config['api_key']


co = cohere.Client(load_token())

tests = pd.read_csv(
    'similarity_ground_truth.csv')

llm_results = pd.DataFrame(columns=['Prompt', 'Actual', 'Expected', 'Precision', 'Recall', 'F1'])

iterations = 0

# for index, row in tqdm(tests.iterrows()):
#     iterations += 1
#     prompt = "Recommend me some movies similar to this movie: " + row['movie']
#     print(prompt)
#     try:
#         result_text, result_titles = get_llm(prompt)
#     except Exception as e:
#         print(e)
#         continue
#     expected_titles_str = row['recs']
#     expected_titles = expected_titles_str.split(" | ")
#     true_positive = 0
#     false_positive = 0
#     false_negative = 0
#     for title in result_titles:
#         if title in expected_titles:
#             true_positive += 1
#         else:
#             false_positive += 1
#     for title in expected_titles:
#         if title not in result_titles:
#             false_negative += 1
#     false_negative = min(12, false_negative)
#
#     if true_positive + false_positive == 0:
#         precision = 0
#     else:
#         precision = true_positive / (true_positive + false_positive)
#
#     if true_positive + false_negative == 0:
#         recall = 0
#     else:
#         recall = true_positive / (true_positive + false_negative)
#
#     if precision + recall == 0:
#         f1 = 0
#     else:
#         f1 = 2 * precision * recall / (precision + recall)
#     print(f"Precision: {precision}")
#     print(f"Recall: {recall}")
#     print(f"F1: {f1}")
#     new_row = pd.DataFrame(
#         {'Prompt': [row['movie']], 'Actual': [len(result_titles)], 'Expected': [len(expected_titles)],
#          'Precision': [precision], 'Recall': [recall], 'F1': [f1]})
#     llm_results = pd.concat([llm_results, new_row], ignore_index=True)
#
#     clear_chat()

# llm_results.to_csv('llm_similarity.csv')

# cluster_results = pd.DataFrame(columns=['Prompt', 'Actual', 'Expected', 'Precision', 'Recall', 'F1'])
# from Flask.app import get_recommendation_cluster
#
# iterations = 0
#
# for index, row in tqdm(tests.iterrows()):
#     iterations += 1
#     title = row['movie']
#     try:
#         result_titles = get_recommendation_cluster(title)
#     except Exception as e:
#         print(e)
#         continue
#     expected_titles_str = row['recs']
#     expected_titles = expected_titles_str.split(" | ")
#     true_positive = 0
#     false_positive = 0
#     false_negative = 0
#     for title in result_titles:
#         if title in expected_titles:
#             true_positive += 1
#         else:
#             false_positive += 1
#     for title in expected_titles:
#         if title not in result_titles:
#             false_negative += 1
#
#     if true_positive + false_positive == 0:
#         precision = 0
#     else:
#         precision = true_positive / (true_positive + false_positive)
#
#     if true_positive + false_negative == 0:
#         recall = 0
#     else:
#         recall = true_positive / (true_positive + false_negative)
#
#     if precision + recall == 0:
#         f1 = 0
#     else:
#         f1 = 2 * precision * recall / (precision + recall)
#     print(f"Precision: {precision}")
#     print(f"Recall: {recall}")
#     print(f"F1: {f1}")
#     new_row = pd.DataFrame(
#         {'Prompt': [row['movie']], 'Actual': [len(result_titles)], 'Expected': [len(expected_titles)],
#          'Precision': [precision], 'Recall': [recall], 'F1': [f1]})
#     cluster_results = pd.concat([cluster_results, new_row], ignore_index=True)
#
# cluster_results.to_csv('cluster_similarity.csv')

tfidf_results = pd.DataFrame(columns=['Prompt', 'Actual', 'Expected', 'Precision', 'Recall', 'F1'])
from Flask.app import get_recommendation_tfidf

iterations = 0

for index, row in tqdm(tests.iterrows()):
    iterations += 1
    title = row['movie']
    try:
        result_titles = get_recommendation_tfidf(title)
    except Exception as e:
        print(e)
        continue
    expected_titles_str = row['recs']
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
        {'Prompt': [row['movie']], 'Actual': [len(result_titles)], 'Expected': [len(expected_titles)],
         'Precision': [precision], 'Recall': [recall], 'F1': [f1]})
    tfidf_results = pd.concat([tfidf_results, new_row], ignore_index=True)

tfidf_results.to_csv('tfidf_similarity.csv')
