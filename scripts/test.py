import pickle
from sklearn.metrics import f1_score
import numpy as np
from sklearn.externals import joblib
import os.path

curr_folder = os.path.dirname(__file__)

with open(os.path.join(curr_folder, '../datasets/X_test.p'), 'rb') as handle:
    X_test = pickle.load(handle)
with open(os.path.join(curr_folder, '../datasets/y_test.p'), 'rb') as handle:
    y_test = pickle.load(handle)

dim_clf = joblib.load(os.path.join(curr_folder, '../pickles/dim_clf.pkl'))

score = dim_clf.score(X_test, y_test)
print("Classifier accuracy: %.3f" % score)

# Print incorrect results
# for i, x in enumerate(X_test):
#     pred = dim_clf.predict([x])
#     if pred != y_test[i]:
#         print(x)
#         print(list(zip(dim_clf.classes_, dim_clf.predict_proba([x])[0])))
#         print(pred, y_test[i], sep='\n')
#         print('\n\n')