import csv
import json
import pickle

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

label_dataset = {}
with open('./OPP-115/pretty_print/amazon.com.csv') as label_file:
    reader = csv.reader(label_file)
    for row in reader:
        annotation_id = row[0]
        label = row[3]
        label_dataset[annotation_id] = label

for row in summary_dataset:
    row['label'] = label_dataset[row['annotation_id']]

pickle.dump(summary_dataset, open('summary_dataset.p', 'wb'))

with open('summary_dataset.p', 'rb') as handle:
    dataset = pickle.load(handle)

print dataset