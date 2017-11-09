import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np

with open('summary_dataset.p', 'rb') as handle:
    dataset = pickle.load(handle)

data = []
targets = []
for item in dataset:
    data.append(item['raw_text'])
    targets.append(item['label'])

# print [[x,targets.count(x)] for x in set(targets)]

text_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', MultinomialNB()),
])

text_clf = text_clf.fit(data, targets)

test_data = ['We get information about you from third parties. For example, if you use an integrated social media feature on our websites or mobile applications. The third-party social media site will give us certain information about you. This could include your name and email address. Your activities on our sites and apps may be posted to the social media platforms.']
predicted = text_clf.predict(test_data)
print predicted