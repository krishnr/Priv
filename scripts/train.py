import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.externals import joblib
import os

curr_folder = os.path.dirname(__file__)

with open(os.path.join(curr_folder, '../datasets/X_train.p'), 'rb') as handle:
    X_train = pickle.load(handle)
with open(os.path.join(curr_folder,'../datasets/y_train.p'), 'rb') as handle:
    y_train = pickle.load(handle)
with open(os.path.join(curr_folder, '../datasets/dim_data.p'), 'rb') as handle:
    dim_data = pickle.load(handle)

clf = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', RandomForestClassifier()),
])

print("Training dimension classifier...")
dim_clf = clf.fit(X_train, y_train)

print("Training answer classifiers...")
ans_clfs = {}
for dim in dim_data:
    clf = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', RandomForestClassifier()),
    ])

    X_train = dim_data[dim]['X_train']
    y_train = dim_data[dim]['y_train']

    ans_clf = clf.fit(X_train, y_train)
    ans_clfs[dim] = ans_clf

folder = os.path.join(curr_folder, '../pickles')
if not os.path.exists(folder):
    print("Making directory: " + folder)
    os.makedirs(folder)

joblib.dump(dim_clf, os.path.join(curr_folder, '../pickles/dim_clf.pkl'))
joblib.dump(ans_clfs, os.path.join(curr_folder, '../pickles/ans_clfs.pkl'))