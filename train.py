import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.externals import joblib

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

joblib.dump(label_clf, 'label_clf.pkl')
joblib.dump(dim_clf, 'dim_clf.pkl')

pickle.dump(label_dict, open('label_dict.p', 'wb'))