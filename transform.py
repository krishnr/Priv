import csv
import json
import pickle

summary_dataset = []

dim_map = {
    'First Party Collection/Use': 'Collection',
    'Third Party Sharing/Collection': 'Use',
    'User Choice/Control': 'Choices',
    'User Access, Edit, & Deletion': 'Choices',
    'Data Retention': 'Disclosure',
    'Data Security': 'Disclosure', 
    'Policy Change': 'Choices',
    'Do Not Track': 'Collection',
}

def build_dataset(a_file, l_file):
    dataset_arr = []
    with open(a_file) as annotation_file:
        reader = csv.reader(annotation_file)
        for row in reader:
            temp_dict = {}
            annotation_id = row[0]
            opp_dimension = row[5]
            attrs = json.loads(row[6])
            raw_text = ''
            for category in attrs:
                if 'selectedText' in attrs[category]:
                    raw_text += ' ' + attrs[category]['selectedText']

            temp_dict['annotation_id'] = annotation_id
            dimension = dim_map[opp_dimension] if opp_dimension in dim_map else 'None'
            temp_dict['dimension'] = dimension
            temp_dict['raw_text'] = raw_text

            dataset_arr.append(temp_dict)

    label_dataset = {}
    with open(l_file) as label_file:
        reader = csv.reader(label_file)
        for row in reader:
            annotation_id = row[0]
            label = row[3]
            label_dataset[annotation_id] = label

    return_arr = []
    removed_labels = [
        'The text introduces the policy, a section, or a group of practices, but it does not mention a specific practice.',
        'The text describes a specific data practice that is not covered by our label scheme.',
        'The policy makes generic security statements, e.g., "we protect your data" or "we use technology/encryption to protect your data".',
        'The text describes how to contact the company with questions, concerns, or complaints about the privacy policy.',
        'The policy makes specific provisions for international audiences, non-US citizens, or non-European citizens (e.g., about international data transfer).',
    ]
    
    for row in dataset_arr:
        if label_dataset[row['annotation_id']] not in removed_labels:
            row['label'] = label_dataset[row['annotation_id']]
            return_arr.append(row)

    return return_arr

atlantic = build_dataset('./OPP-115/annotations/20_theatlantic.com.csv', './OPP-115/pretty_print/theatlantic.com.csv')
summary_dataset += atlantic

wapo = build_dataset('./OPP-115/annotations/200_washingtonpost.com.csv', './OPP-115/pretty_print/washingtonpost.com.csv')
summary_dataset += wapo

thehill = build_dataset('./OPP-115/annotations/1360_thehill.com.csv', './OPP-115/pretty_print/thehill.com.csv')
summary_dataset += thehill


pickle.dump(summary_dataset, open('summary_dataset.p', 'wb'))

with open('summary_dataset.p', 'rb') as handle:
    dataset = pickle.load(handle)

print dataset