import os
import csv
import re



def get_dimension(label, dimension):
    dim_map = {
    'First Party Collection/Use': 'Collection',
    'Third Party Sharing/Collection': 'Third Party',
    'User Choice/Control': 'Choices',
    'User Access, Edit and Deletion': 'Choices',
    'Data Retention': 'Storage',
    'Data Security': 'Storage', 
    'Policy Change': 'Choices',
    'Do Not Track': 'Do Not Track',
    'International and Specific Audiences': 'International',
    'Other': 'Other'
    }
    
    if 'location' in label.lower():
        return 'Location'

    return dim_map[dimension]

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
        return_arr.append((row['label'], dimension))

    return return_arr

labels_list = []

label_directory = '../OPP-115/pretty_print/'
annotation_directory = '../OPP-115/annotations/'

for filename in os.listdir(annotation_directory):
    match = re.search('[\d]+_(.+)', filename)
    label_name = match[1]
    l_file = label_directory + label_name
    a_file = annotation_directory + filename
    labels_list += build_dataset(a_file, l_file)

labels_list = list(set(labels_list))

with open('../labels_list.csv', 'w') as f:
    wr = csv.writer(f,delimiter=',')
    for line in labels_list:
        wr.writerow(line)