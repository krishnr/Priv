from flask import Flask, jsonify, request
from sklearn.externals import joblib
from collections import Counter
import pickle
import get_policies


app = Flask(__name__)


def is_valid_line(line):
    # Assuming a heading (which we want to ignore) is less than 50 chars
    return len(line) > 100

@app.route("/summarize")
def summarize():
    hostname = request.args.get('hostname')
    print(hostname)

    # Find the right file based on the website we're on
    policy = get_policies.get_policy(hostname)

    label_clf = joblib.load('./pickles/label_clf.pkl')
    dim_clf = joblib.load('./pickles/dim_clf.pkl')

    with open('./pickles/label_dict.p', 'rb') as handle:
        label_dict = pickle.load(handle)

    pp_lines = []
    for line in policy.split('\n'):
        if is_valid_line(line):
            pp_lines.append(line)

    predicted_dims = dim_clf.predict(pp_lines)

    relevant_lines = []
    for i, elem in enumerate(predicted_dims):
        if elem != 'None':
            relevant_lines.append(pp_lines[i])

    predicted_labels = label_clf.predict(relevant_lines)

    # print lines with associated labels
    #for i, elem in enumerate(predicted_labels):
        #print relevant_lines[i] + "   :   " + elem
        #print "\n"


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

    return jsonify({
        'collection': { # (What information is being collected?) (Notice, Consent)
            'score': 1, 
            'more_info': {
                'label_1': collection_labels[0] if len(collection_labels) >= 1 else " ",
                'label_2': collection_labels[1] if len(collection_labels) >= 2 else " ",
                'label_3': collection_labels[2] if len(collection_labels) >= 3 else " "
            }
        },
        'use': { # (How is this information being used?) (Purpose)
            'score': 2, 
            'more_info': {
                'label_1': use_labels[0] if len(use_labels) >= 1 else " ",
                'label_2': use_labels[1] if len(use_labels) >= 2 else " ",
                'label_3': use_labels[2] if len(use_labels) >= 3 else " "
            }
        }, 
        'disclosure': { # Disclosure/Information Sharing (Who has access to this data?) (Disclosure, Security)
            'score': 3, 
            'more_info': {
                'label_1': disclosure_labels[0] if len(disclosure_labels) >= 1 else " ",
                'label_2': disclosure_labels[1] if len(disclosure_labels) >= 2 else " ",
                'label_3': disclosure_labels[2] if len(disclosure_labels) >= 3 else " "
            }
        },
        'choice': { # Choices (What can you do if policy isn't followed?) (Accountability)
            'score': 4, 
            'more_info': {
                'label_1': choices_labels[0] if len(choices_labels) >= 1 else " ",
                'label_2': choices_labels[1] if len(choices_labels) >= 2 else " ",
                'label_3': choices_labels[2] if len(choices_labels) >= 3 else " "
            }
        }
    })


