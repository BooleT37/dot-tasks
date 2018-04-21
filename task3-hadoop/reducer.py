#!/usr/bin/python3

import sys
from itertools import groupby
from operator import itemgetter


def read_mapper_output(file, separator="\t"):
    for line in file:
        yield line.strip().split(separator)

def reduce_mapper_output(separator="\t"):
    # maps words to their counts
    ngram2count = {}
    ngram3count = {}

    data = read_mapper_output(sys.stdin, separator=separator)

    for ngram3, count3, ngram2, count2 in data:
        count2 = int(count2)
        count3 = int(count3)
        if ngram2 in ngram2count:
            ngram2count[ngram2] += count2
        else:
            ngram2count[ngram2] = count2

        if ngram3 in ngram3count:
            ngram3count[ngram3] += count3
        else:
            ngram3count[ngram3] = count3

    for ngram3 in ngram3count.keys():
        words = ngram3.split(" ")
        try:
            ngram2 = " ".join(words[0:2])
            sys.stdout.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(
                words[0], words[1], words[2], 
                ngram3count[ngram3],
                ngram2count[ngram2],
                float(ngram3count[ngram3]) / float(ngram2count[ngram2])))
        except:
            continue
            # ??? len(words) != 3


if __name__ == "__main__":
    reduce_mapper_output()
