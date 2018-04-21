import os
import sys

def read_input(file):
    for line in file:
        line = line.strip()
        words = line.split()
        words = list(map(lambda x: x.lower(), words))
        if len(words) < 3:
            continue

        for i in range(len(words)-2):
            yield [" ".join(words[i:i+3]), " ".join(words[i:i+2])]

def parse_input(file, separator="\t"):
    for ngram in read_input(file):
        sys.stdout.write("{0}\t{1}\n".format(ngram[0], 1, ngram[1], 1))


if __name__ == "__main__":
    with open(os.path.join("input", "5000-8.txt")) as f:
        parse_input(f)
