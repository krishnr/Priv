from flask import Flask, jsonify, request
from sklearn.externals import joblib
from collections import Counter
import pickle
from . import get_policies
import os.path
from operator import itemgetter
from . import get_question
import nltk

nltk.download('punkt')

app = Flask(__name__)
curr_folder = os.path.dirname(__file__)


def is_valid_line(line):
    # Assuming a heading (which we want to ignore) is less than 50 chars
    return len(line) > 100


def tokenize_into_sentences(policy):
    pp_lines = nltk.sent_tokenize(policy)
    return pp_lines


@app.route("/summarize")
def summarize():
    hostname = request.args.get('hostname')
    print(hostname)

    # Find the right file based on the website we're on
    policy = get_policies.get_policy(hostname)
    dim_clf = joblib.load(os.path.join(curr_folder, '../pickles/dim_clf.pkl'))
    ans_clfs = joblib.load(os.path.join(curr_folder, '../pickles/ans_clfs.pkl'))

    pp_lines = tokenize_into_sentences(policy)

    predicted_dims = dim_clf.predict(pp_lines)

    scores = dim_clf.predict_proba(pp_lines)
    
    predictions = []
    for i, dim in enumerate(predicted_dims):
        dim_index = list(dim_clf.classes_).index(dim)
        predictions.append([pp_lines[i], dim, scores[i][dim_index]])
    
    # sort predictions by score
    predictions = sorted(predictions, key=itemgetter(2))
    predictions = predictions[::-1]
    
    # get up to 7 different dimensions
    top_preds = []
    score = 1
    i = 0
    dims = []
    while len(top_preds) < 7 and score > 0.5 and i < len(predictions):
        score = predictions[i][2]
        dim = predictions[i][1]
        if dim not in dims:
            top_preds.append(predictions[i])
            dims.append(dim)
        i += 1

    # predict Yes/No/Maybe
    for pred in top_preds:
        dim = pred[1]
        raw_text = pred[0]
        ans = ans_clfs[dim].predict([raw_text])[0].lower()
        pred.append(ans)
        pred.append(raw_text)
    
    output = {
        "summary": {},
        "action": "https://advocacy.mozilla.org/en-US/privacynotincluded"
    }
    
    # construct output
    for pred in top_preds:
        question = get_question.get_question(pred[1])
        ans = pred[3]
        raw_text = pred[4]
        output["summary"][question] = [ans, raw_text]
    
    print(output)
    return jsonify(output)


