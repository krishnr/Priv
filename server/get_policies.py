"""
    Handles retrieving policies from:
    ACL/COLING 2014 Dataset Zip File
    Policies Directory
    Scraped from webpage
"""
from zipfile import ZipFile
import re
import pickle


def get_policy(hostname):
    with open('../policies/corpus.pkl', 'rb') as pkl:
        # Check if webpage is in corpus zip file
        corpus_list = pickle.load(pkl)
        r = re.compile('corpus/.*{}.*\.xml'.format(hostname))
        results = list(filter(r.match, corpus_list))
        if results:
            # Get first result for now
            result = results[0]
            with ZipFile('../policies/corpus.zip', 'r') as archive:
                with archive.open(result, 'r') as file:
                    file_bytes = file.read()
                    # Remove tags and clean up whitespace issues
                    remove_tags = re.compile(b'<.*>')
                    file_bytes = re.sub(remove_tags, b'', file_bytes)
                    file_bytes = re.sub(b'\n\s*\n', b'\n', file_bytes)
                    file_bytes = re.sub(b' {2,}', b'', file_bytes)

                    print(file_bytes.decode('utf-8'))
                    # with open('test.txt', 'w') as test:
                    #     test.write(file_bytes.decode('utf-8'))

get_policy('mashable')