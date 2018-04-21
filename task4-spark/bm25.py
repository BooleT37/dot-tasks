#!venv/bin/python3
# -*- coding: utf-8

import os
import sys
import json
from collections import Counter
from pyspark import SparkContext


current_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_path, "opencorpora")
data_js = os.path.join(current_path, "opencorpora_json") 

N = 4062
b = 0.5
k = 1.2


def doc_len(file_name):
    """
    Finds document length
    """
    with open(os.path.join(data_path, file_name), "r") as f:
        return len(f.read())

def get_entries(file_name, query):
    """
    Searchs for the query words in document
    Returns {query_word_1: 0, query_word_2: 5, ....} 
    where values are the number of occurances of the query word i in document
    """
    with open(os.path.join(current_path, data_js, file_name + ".json"), "r") as fp:
        d = json.load(fp)
        return {word: min(d.setdefault(word, 0), 1) for word in query}


def get_score(file_name, query, words_dict, avg_length):
	
    def idf(word, words_dict):
        """
        Helper function for IDF calculation
        """
        return (N - words_dict.setdefault(word, 0) + 0.5) / (words_dict.setdefault(word) + 0.5)
    
    q_idf = {w: idf(w, words_dict) for w in query}

    with open(os.path.join(data_js, file_name + ".json"), "r") as fp:
        with open(os.path.join(data_path, file_name), "r") as f:
            d = json.load(fp)
            c = f.read()
            score = sum([
                ( (d.setdefault(w, 0) * (k + 1)) / (d.setdefault(w, 0) + k * (1 - b + b * len(c) / avg_length)) ) * q_idf[w] 
                for w in query
            ])
            return file_name, score


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python3 bm25.py 'my query'")
        exit(-1)

   
    sc = SparkContext()


    query = sc.textFile(sys.argv[1], 1)
    query_list = sys.argv[1].split(" ")

    files = sc.parallelize([
        f for f in os.listdir(data_path) 
        if os.path.isfile(os.path.join(data_path, f))
    ])

    avg_length = sum(files.map(doc_len).collect()) / N

    num_of_entries = {}
    
    occurances = files.map(lambda f: get_entries(f, query_list))
    # occurances.collect() --> [{w1: n1, w2: n2}, {w1: m1, w2: m2}, ...]
    #                            for file1         for file2

    ne = [Counter(d) for d in occurances.collect()]
    ad = ne[0] # Counter for file1


    # For each word calculate the number of occurances in the corpora
    for i in range(1, len(ne)):
        ad += ne[i]
    
    
    scores = (
        files \
        .map(lambda file: get_score(file, query_list, dict(ad), avg_length)) \
        .collect()
    )

    results = sorted(scores, key=lambda x: x[1], reverse=True)

    print("{0}\t{1}".format("Document", "Score"))

    for x in results[:10]:
        print("{0}\t{1}".format(x[0], x[1]))
    
    sc.stop()
