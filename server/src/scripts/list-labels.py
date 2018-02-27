import os
import csv
import re

dim_list = []
def get_dimension(label, dimension):
    dim_map = {
    'First Party Collection/Use': 'Collection',
    'Third Party Sharing/Collection': 'Third Party',
    'User Choice/Control': 'Choices',
    'User Access, Edit and Deletion': 'Choices',
    'Data Retention': 'Retention',
    'Data Security': 'Security', 
    'Policy Change': 'Choices',
    'Do Not Track': 'Do Not Track',
    'International and Specific Audiences': 'International',
    'Other': 'Other'
    }
    
    if 'location' in label.lower():
        return 'Location'
    
    if 'ip address' in label.lower():
        return 'IP Address'
    
    if 'targeted advertising' in label.lower():
        return 'Targeted Advertising'
    
    if any(s in label.lower() for s in ['change', 'update', 'notif']) or dimension == 'Policy Change':
        return 'Policy Change'

    if dimension == 'Do Not Track':
        return 'Do Not Track'
    
    if dimension == 'Data Security':
        return 'Security'
    
    if any(s in label.lower() for s in ['opt out', 'link']):
        return 'Action'

    if 'financial' in label.lower():
        return 'Payment'
    
    if any(s in label.lower() for s in ['legal', 'law']):
        return 'Disclosure'
    
    if 'health' in label.lower():
        return 'Health'
    
    if all(s in label.lower() for s in ['delete', 'account']):
        return 'Deletion'
    
    if 'social media' in label.lower():
        return 'Social Media'

    if 'device id' in label.lower():
        return 'Identification'
    
    if any(s in label.lower() for s in ['personalization', 'customization']):
        return 'Personalization'
    
    if 'cookies' in label.lower():
        return 'Cookies'

    if any(s in label.lower() for s in ['demographic', 'analytics', 'research', 'identifiable']):
        if 'third party' in label.lower():
            return '3P Analysis'
        else:
            return '1P Analysis'

    return None

def build_dataset(a_file, l_file):
    dataset_arr = []
    with open(a_file) as annotation_file:
        reader = csv.reader(annotation_file)
        for row in reader:
            temp_dict = {}
            annotation_id = row[0]
            opp_dimension = row[5]

            temp_dict['annotation_id'] = annotation_id
            temp_dict['dimension'] = opp_dimension

            dataset_arr.append(temp_dict)

    label_dataset = {}
    with open(l_file) as label_file:
        reader = csv.reader(label_file)
        for row in reader:
            annotation_id = row[0]
            label = row[3]
            label_dataset[annotation_id] = label

    return_arr = []
    
    for row in dataset_arr:
        row['label'] = label_dataset[row['annotation_id']]
        dimension = get_dimension(row['label'], row['dimension'])
        if not dimension:
            continue
        dim_list.append(dimension)
        return_arr.append((row['label'], dimension))

    return return_arr

labels_list = []

label_directory = '../../OPP-115/pretty_print/'
annotation_directory = '../../OPP-115/annotations/'


for filename in os.listdir(annotation_directory):
    match = re.search('[\d]+_(.+)', filename)
    label_name = match[1]
    l_file = label_directory + label_name
    a_file = annotation_directory + filename
    label_tuple = build_dataset(a_file, l_file)
    labels_list += label_tuple

labels_list = list(set(labels_list))

counts =  [(x, dim_list.count(x)) for x in set(dim_list)]
print(counts)

with open('../../labels_list.csv', 'w') as f:
    wr = csv.writer(f,delimiter=',')
    for line in labels_list:
        wr.writerow(line)