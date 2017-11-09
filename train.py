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

# counts =  [targets.count(x) for x in set(targets)]
# counts.sort(reverse=True)
# print counts

text_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', MultinomialNB(fit_prior=False)),
])

text_clf = text_clf.fit(data, targets)

test_data = [
    'Registration for the NYT Services may require that you supply certain personal information, including a unique email address and demographic information (ZIP code, age, sex, household income, job industry and job title) to register.',

    "Billing and Credit Card Information To enable payment and donations via the NYT Services, we collect and store name, address, telephone number, email address, credit card information and other billing information",
    
    "The ads in our apps are not targeted to you based on your current GPS location, but they may be targeted to you based on your ZIP code or device's IP address.",

    "COPPA Compliance. The New York Times does not knowingly collect or store any personal information about children under the age of 13.",


]

predicted = text_clf.predict(test_data)
print predicted