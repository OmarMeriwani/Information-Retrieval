'''import importlib
moduleName = input('search.py')
pm = __import__(moduleName)
from pm import  index_corpus, search, tf_idf'''
from search import index_corpus, search, tf_idf
import glob

def calc_precision(tp, fp):
  if tp + fp == 0:
    return 0
  return tp / float(tp + fp)

def calc_recall(tp, fn):
  if tp + fn == 0:
    return 0
  return tp / float(tp + fn)

def calc_fmeasure(precision, recall):
  if precision + recall == 0:
    return 0
  return 2 * ((precision * recall)/(precision + recall))

files = glob.glob("*.txt")

rows = [line.strip().split(",") for line in open("evaluation.csv","r").readlines()]
index_corpus()

print ("""
True Positive: One we got correct
False Positive: One we though was right, but was wrong
False Negative: One we missed
""")

def display_result_list(label, results):
  return label + ": " + "; ".join(results)

for row in rows:
  search_terms = row[0]
  expected = set(row[1:])
  results = search(search_terms, term_weighting_scheme=tf_idf)
  received =[result[0] for result in results] # get rid of the scores for now
  print ("-" * 50)
  print ("searched for:", search_terms)
  print (display_result_list("expected", expected))
  print (display_result_list("received", received))
  received = set(received)

  true_positives = expected & received
  false_negatives = expected - received
  false_positives = received - expected
  print (display_result_list("\ttrue positives", true_positives))
  print (display_result_list("\tfalse positives", false_positives))
  print (display_result_list("\tfalse negatives", false_negatives))

  precision = calc_precision(len(true_positives), len(false_positives))
  recall = calc_recall(len(true_positives), len(false_negatives))
  fmeasure = calc_fmeasure(precision, recall)
  print ("precision: ", precision, "recall: ", recall, "f-measure: ", fmeasure)
