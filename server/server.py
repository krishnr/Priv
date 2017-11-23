from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def summarize():
    # return "hi krishn"
    return jsonify({
        'collection': { # (What information is being collected?) (Notice, Consent)
            'score': 1, 
            'more_info': {
                'label_1': "bananas",
                'label_2': "blah2",
                'label_3': "blah3"
            }
        },
        'use': { # (How is this information being used?) (Purpose)
            'score': 2, 
            'more_info': {
                'label_1': "bananas",
                'label_2': "blah2",
                'label_3': "blah3"
            }
        }, 
        'disclosure': { # Disclosure/Information Sharing (Who has access to this data?) (Disclosure, Security)
            'score': 3, 
            'more_info': {
                'label_1': "blah1",
                'label_2': "bannaas",
                'label_3': "blah3"
            }
        },
        'choice': { # Choices (What can you do if policy isn't followed?) (Accountability)
            'score': 4, 
            'more_info': {
                'label_1': "blah1",
                'label_2': "bananas",
                'label_3': "blah3"
            }
        }
    })


