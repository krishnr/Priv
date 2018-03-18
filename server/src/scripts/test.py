import pickle
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import numpy as np
from sklearn.externals import joblib
import os.path

curr_folder = os.path.dirname(__file__)

with open(os.path.join(curr_folder, '../../datasets/X_test.p'), 'rb') as handle:
    X_test = pickle.load(handle)
with open(os.path.join(curr_folder, '../../datasets/y_test.p'), 'rb') as handle:
    y_test = pickle.load(handle)
with open(os.path.join(curr_folder, '../../datasets/X_train.p'), 'rb') as handle:
    X_train = pickle.load(handle)
with open(os.path.join(curr_folder,'../../datasets/y_train.p'), 'rb') as handle:
    y_train = pickle.load(handle)
with open(os.path.join(curr_folder, '../../datasets/dim_data.p'), 'rb') as handle:
    dim_data = pickle.load(handle)

dim_clf = joblib.load(os.path.join(curr_folder, '../../pickles/dim_clf.pkl'))
ans_clfs = joblib.load(os.path.join(curr_folder, '../../pickles/ans_clfs.pkl'))

print(len(X_train))
print(len(X_test))

score = dim_clf.score(X_test, y_test)
print("Dimension classifier accuracy: %.3f" % score)
y_pred = dim_clf.predict(X_test)
score = precision_score(y_test, y_pred, average="macro")
print("Dimension classifier precision: %.3f" % score)
score = recall_score(y_test, y_pred, average="macro")
print("Dimension classifier recall: %.3f" % score)
print("\n")

accuracies = []
precisions = []
recalls = []
for dim in dim_data:
    X_test = dim_data[dim]['X_test']
    y_test = dim_data[dim]['y_test']
    score = ans_clfs[dim].score(X_test, y_test)
    accuracies.append(score)
    print("Answer classifier accuracy for %s: %.3f" % (dim, score))
    y_pred = ans_clfs[dim].predict(X_test)
    score = precision_score(y_test, y_pred, average="macro")
    precisions.append(score)
    print("Answer classifier precision for %s: %.3f" % (dim, score))
    score = recall_score(y_test, y_pred, average="macro")
    recalls.append(score)
    print("Answer classifier recall for %s: %.3f" % (dim, score))
    print("\n")

print(np.mean(accuracies))
print(np.mean(precisions))
print(np.mean(recalls))

# Print incorrect results
# for i, x in enumerate(X_test):
#     pred = dim_clf.predict([x])
#     if pred != y_test[i]:
#         print(x)
#         print(list(zip(dim_clf.classes_, dim_clf.predict_proba([x])[0])))
#         print(pred, y_test[i], sep='\n')
#         print('\n\n')