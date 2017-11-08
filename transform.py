import csv
import json

summary_dataset = []

with open('./OPP-115/annotations/105_amazon.com.csv') as amzn:
    reader = csv.reader(amzn)
    for row in reader:
        temp_dict = {}
        annotation_id = row[0]
        dimension = row[5]
        attrs = json.loads(row[6])
        raw_text = ''
        for category in attrs:
            if 'selectedText' in attrs[category]:
                raw_text += ' ' + attrs[category]['selectedText']

        temp_dict['annotation_id'] = annotation_id
        temp_dict['dimension'] = dimension
        temp_dict['raw_text'] = raw_text

        summary_dataset.append(temp_dict)