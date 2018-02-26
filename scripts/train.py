import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
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

dim_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      #('clf', MultinomialNB(fit_prior=False)),
                      ('clf', RandomForestClassifier()),
])

print("Training classifier...")
dim_clf = dim_clf.fit(X_train, y_train)

folder = os.path.join(curr_folder, '../pickles')
if not os.path.exists(folder):
    print("Making directory: " + folder)
    os.makedirs(folder)

joblib.dump(dim_clf, os.path.join(curr_folder, '../pickles/dim_clf.pkl'))