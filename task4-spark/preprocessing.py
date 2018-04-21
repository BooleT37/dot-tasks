#!venv/bin/python3

import os
import json
from pyspark import SparkContext


current_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_path, "opencorpora")
data_js = os.path.join(current_path, "opencorpora_json") 

sc = SparkContext()

files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]

if not os.path.exists(data_js):
    os.makedirs(data_js)

for f in files:
    text_file = sc.textFile(os.path.join(data_path, f), 1)
    counts = text_file \
    	.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word.lower(), 1)) \
        .reduceByKey(lambda a, b: a + b)

    with open(os.path.join(data_js, f + ".json"), "w+") as fp:
        json.dump(counts.collectAsMap(), fp)

sc.stop()
