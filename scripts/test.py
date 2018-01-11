import pickle
from sklearn.metrics import f1_score
import numpy as np
from sklearn.externals import joblib

with open('datasets/test_dataset.p', 'rb') as handle:
    test_dataset = pickle.load(handle)

raw_text = []
dim_targets = []
label_targets = []
for item in test_dataset:
    raw_text.append(item['raw_text'])
    dim_targets.append(item['dimension'])
    label_targets.append(item['label'])

label_clf = joblib.load('pickles/label_clf.pkl')
dim_clf = joblib.load('pickles/dim_clf.pkl')

predicted_labels = label_clf.predict(raw_text)


print f1_score(label_targets, predicted_labels, average=None)