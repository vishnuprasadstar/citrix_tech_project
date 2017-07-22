import csv
import random
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

data = {}

def load(filename):
	with open(filename) as f:
		for line in f:
			(key, val) = line.split()
			data[key] = float(val)

def query(line):
	smoothing = 0.1
	probablity = 1.0
	stop_words = set(stopwords.words("english"))
	words = word_tokenize(line)
	words = filter(lambda x: x not in string.punctuation, words)
	words = filter(lambda x: x not in stop_words, words)
	for w in words:
		tmp = smoothing
		if w in data.keys():
			tmp = data[w];
		probablity = probablity*tmp
	return probablity

def main():
	filename = 'Data.csv'
	load(filename)
        import ipdb; ipdb.set_trace()
	print query("buy my product")
