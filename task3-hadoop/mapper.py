#!/usr/bin/python3

import sys


def read_input(file):
    for line in file:
        line = line.strip()
        words = line.split()
        words = list(map(lambda x: x.lower(), words))

        if len(words) < 2:
            continue

        for i in range(len(words)-1):
            yield (" ".join(words[i:i+3]), " ".join(words[i:i+2]))

def parse_input(separator="\t"):
    for ngram in read_input(sys.stdin):
        sys.stdout.write("{0}\t{1}\t{2}\t{3}\n".format(ngram[0], 1, ngram[1], 1))

if __name__ == "__main__":
    parse_input()
