import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
from collections import Counter

with open('summary_dataset.p', 'rb') as handle:
    dataset = pickle.load(handle)

raw_text = []
dim_targets = []
label_targets = []
label_dict = {}
for item in dataset:
    raw_text.append(item['raw_text'])
    dim_targets.append(item['dimension'])
    # if item['dimension'] == 'None':
    #     label_targets.append('None')
    # else:
    label_targets.append(item['label'])
    label_dict[item['label']] = item['dimension']

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
f = open("policies/NYT.txt", "r")

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

# print lines with associated labels
for i, elem in enumerate(predicted_labels):
    print relevant_lines[i] + "   :   " + elem
    print "\n"


predicted_labels = predicted_labels.tolist()
# sorting labels by number of occurences
predicted_labels.sort(key=Counter(predicted_labels).get, reverse=True)
# keeping only unique labels
predicted_labels = list(set(predicted_labels))

collection_labels = []
i = 0
while(len(collection_labels) < 3 and i < len(predicted_labels)):
    label = predicted_labels[i]
    if (label_dict[label] == 'Collection'):
        collection_labels.append(label)
    i += 1

use_labels = []
i = 0
while(len(use_labels) < 3 and i < len(predicted_labels)):
    label = predicted_labels[i]
    if (label_dict[label] == 'Use'):
        use_labels.append(label)
    i += 1

disclosure_labels = []
i = 0
while(len(disclosure_labels) < 3 and i < len(predicted_labels)):
    label = predicted_labels[i]
    if (label_dict[label] == 'Disclosure'):
        disclosure_labels.append(label)
    i += 1

choices_labels = []
i = 0
while(len(choices_labels) < 3 and i < len(predicted_labels)):
    label = predicted_labels[i]
    if (label_dict[label] == 'Choices'):
        choices_labels.append(label)
    i += 1

print collection_labels
print use_labels
print disclosure_labels
print choices_labels