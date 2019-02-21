import glob 
import re
import math
from collections import defaultdict
import sys

identity = lambda x: x

doc_freq = {}
term_vec = []
forward_index = {} # documnets => words: their frequencies
inverted_index = defaultdict(set) # words => documents that contain that word

def tokenize(data):
  return re.compile("\s*").split(data)

def preprocess_token(data):
  # a real search engine would do lots of other things here, including stemming
  return data.lower()

def read_files():
  for file_name in glob.glob('*.txt'):
    file_handle = open(file_name, 'r')
    file_contents = file_handle.read()
    yield (file_name, file_contents)

def index_corpus():
  terms = set()
  for file_name, file_contents in read_files():
    forward_index[file_name] = defaultdict(int)
    for token in tokenize(file_contents):
      token = preprocess_token(token)
      terms.add(token)
      forward_index[file_name][token] += 1
      inverted_index[token].add(file_name)
  term_vec.extend(terms)

def doc_to_vec(doc):
  vec = [0] * len(term_vec)
  for i, term in enumerate(term_vec):
    if term in doc:
      vec[i] = doc[term]
  return vec

def idf(term):
  return math.log(len(inverted_index)/len(inverted_index[term]))

def tf_idf(doc_vec):
  vec = [0] * len(term_vec)
  for i, term in enumerate(term_vec):
    tf = doc_vec[i] # raw frequency
    vec[i] = tf * idf(term)
  return vec

def query_to_vec(query_string):
  token_freq = defaultdict(int)
  for token in tokenize(query_string):
    token = preprocess_token(token)
    token_freq[token] += 1
  return doc_to_vec(token_freq)

def cosine_similarity(vec_a, vec_b):
  dp = sum([a * b for a, b in zip(vec_a, vec_b)])
  mag_a, mag_b = [math.sqrt(sum([n ** 2 for n in vec])) for vec in [vec_a, vec_b]]
  if mag_a == 0 or mag_b == 0:
    return 0
  return dp / (mag_a * mag_b)

def search(query, term_weighting_scheme = identity):
  """
  perform a query
  try different term weighting schemes: tf_idf, identity
  """
  query_vec = term_weighting_scheme(query_to_vec(query))
  results = []
  for file_name, doc in forward_index.items():
    doc_vec = term_weighting_scheme(doc_to_vec(doc))
    result = (file_name, cosine_similarity(query_vec, doc_vec))
    if result[1] > 0:
      results.append(result)
  return sorted(results, key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
  index_corpus()
  if len(sys.argv) == 1:
    print (sys.argv[0], "\"<search terms>\"")
  else:
    results = search(sys.argv[1], term_weighting_scheme=tf_idf)
    #print "searching: ", sys.argv[1]
    for file_name, score in results:
      print (file_name, score)
