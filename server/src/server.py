from flask import Flask, jsonify, request, render_template
from sklearn.externals import joblib
from .get_policies import get_policy
import os.path
from operator import itemgetter
from .questions_copy import get_question
from .questions_copy import get_question_desc
from flask_sqlalchemy import SQLAlchemy
import nltk
import time
from sqlalchemy.sql import func
from .util import settings

nltk.download('punkt')
curr_folder = os.path.dirname(__file__)
DBHOST = 'db'
DBPORT = '5432'
settings.load_env()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=os.getenv("POSTGRES_USER"),
        passwd=os.getenv("POSTGRES_PASSWORD"),
        host=DBHOST,
        port=DBPORT,
        db=os.getenv("POSTGRES_DB"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Summary(db.Model):
    domain = db.Column(db.String, primary_key=True)
    summary = db.Column(db.JSON)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, domain, summary):
        self.domain = domain
        self.summary = summary


def create_db():
    # Clear any existing rows in table
    db.drop_all()
    db.create_all()
    test_summary = {
                       "q1": "a1",
                       "q2": "a2",
                   },
    test_entry = Summary('ramandeep', test_summary)
    db.session.add(test_entry)
    db.session.rollback()
    db.session.commit()


def is_valid_line(line):
    # Assuming a heading (which we want to ignore) is less than 50 chars
    return len(line) > 100


def tokenize_into_sentences(policy):
    pp_lines = nltk.sent_tokenize(policy)
    return pp_lines


def get_summary(hostname):
    summary = {}

    result = Summary.query.filter_by(domain=hostname).first()
    if result:
        print("Retrieved: {} from db", hostname)
        summary = result.summary
    else:
        # Find the right file based on the website we're on
        policy = get_policy(hostname)
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

        # get up to num_dims different dimensions
        num_dims = 22
        top_preds = []
        score = 1
        i = 0
        dims = []
        while len(top_preds) < 22 and score > 0.5 and i < len(predictions):
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

        # construct output
        for pred in top_preds:
            question = get_question(pred[1])
            question_desc = get_question_desc(pred[1])
            ans = pred[3]
            raw_text = pred[4]
            summary[question] = [ans, question_desc, raw_text]

        # Add to db
        db.session.add(Summary(hostname, summary))
        db.session.commit()

        print(summary)
    return summary


# Create the database
dbstatus = False

while not dbstatus:
    try:
        create_db()
    except:
        time.sleep(2)
    else:
        print("Instantiated database")
        dbstatus = True


@app.route("/summarize")
def summarize():
    hostname = request.args.get('hostname')
    print("Summarizing {}".format(hostname))

    summary = get_summary(hostname)
    output = {
        "summary": summary,
        "action": "http://mypriv.ca/full_summary/{}".format(hostname)
    }
    print(output)
    return jsonify(output)


@app.route("/full_summary/<hostname>")
def full_summary(hostname):
    print("Retrieving full summary for: {}".format(hostname))
    return render_template('full_summary.html', summary=get_summary(hostname), hostname=hostname)


@app.route("/")
def main():
    return render_template('landing_page.html')
