import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np

with open('summary_dataset.p', 'rb') as handle:
    dataset = pickle.load(handle)

raw_text = []
dim_targets = []
label_targets = []
for item in dataset:
    raw_text.append(item['raw_text'])
    dim_targets.append(item['dimension'])
    # if item['dimension'] == 'None':
    #     label_targets.append('None')
    # else:
    label_targets.append(item['label'])

# counts =  [label_targets.count(x) for x in set(label_targets)]
# counts.sort(reverse=True)
# print counts

dim_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', MultinomialNB(fit_prior=False)),
])

dim_clf = dim_clf.fit(raw_text, dim_targets)

label_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', MultinomialNB(fit_prior=False)),
])

label_clf = label_clf.fit(raw_text, label_targets)

# Find the right file based on the website we're on
f = open("NYT-pp.txt", "r")

def is_valid_line(line):
    line = line.strip("\n")
    # Assuming a heading (which we want to ignore) is less than 50 chars
    return len(line) > 50

pp_lines = []
for line in f:
    if is_valid_line(line):
        pp_lines.append(line)

predicted_dims = dim_clf.predict(pp_lines)

relevant_lines = []
for i, elem in enumerate(predicted_dims):
    if elem != 'None':
        relevant_lines.append(pp_lines[i])

predicted_labels = label_clf.predict(relevant_lines)

for i, elem in enumerate(predicted_labels):
    print relevant_lines[i] + "   :   " + elem
    print "\n"