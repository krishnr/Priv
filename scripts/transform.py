import os
import csv
import re
import json
import pickle
from sklearn.model_selection import train_test_split

curr_folder = os.path.dirname(__file__)

dim_list = []
def get_dimension(label, dimension):
    """
    Assigns labels to Priv dimensions:
    - Identification
    - Targeted Advertising
    - Policy Change
    - Do Not Track
    - Security
    - Retention
    - Action
    - Location
    - Payment
    - Disclosure
    - Health
    - Activity
    - Deletion
    - Social Media
    - Personalization
    - Contact Info
    - Personal Info
    - 3P Analysis
    - 1P Analaysis
    - 3P Collection
    - 1P Collection
    - Cookies
    """

    # Map of OPP 115 dimensions (not used anywhere--just for reference)
    # Most of these are accounted for except for International and Other
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
    
    #### Rules for assigning labels to Priv dimensions

    if any(s in label.lower() for s in ['ip address', 'device id']):
        return 'Identification'
    
    if 'targeted advertising' in label.lower():
        return 'Targeted Advertising'
    
    if any(s in label.lower() for s in ['change', 'update', 'notif']) or dimension == 'Policy Change':
        return 'Policy Change'

    if dimension == 'Do Not Track':
        return 'Do Not Track'
    
    if dimension == 'Data Security':
        return 'Security'
    
    if dimension == 'Data Retention' or 'is retained' in label.lower():
        return 'Retention'
    
    if any(s in label.lower() for s in ['opt out', 'link', 'configuration', 'their information', 'deactivate', 'settings', 'choice', 'access', 'choose not to use', 'contact the company']):
        return 'Action'
    
    if 'location' in label.lower():
        return 'Location'

    if any(s in label.lower() for s in ['financial', 'payment']):
        return 'Payment'
    
    if any(s in label.lower() for s in ['legal', 'law']):
        return 'Disclosure'
    
    if 'health' in label.lower():
        return 'Health'
    
    if 'activities' in label.lower():
        return 'Activity'

    if all(s in label.lower() for s in ['delete', 'account']):
        return 'Deletion'
    
    if 'social media' in label.lower():
        return 'Social Media'
    
    if any(s in label.lower() for s in ['personalization', 'customization']):
        return 'Personalization'

    if 'contact information' in label.lower():
        return 'Contact Info'

    if any(s in label.lower() for s in ['demographic', 'identifiable', 'personal', 'profile']):
        return 'Personal Info'

    if any(s in label.lower() for s in ['analytics', 'research', 'aggregated', 'anonymized', 'survey']):
        if 'third party' in label.lower():
            return '3P Analysis'
        else:
            return '1P Analysis'

    if 'cookies' in label.lower():
        return 'Cookies'

    if any(s in label.lower() for s in ['collect', 'information about you', 'collection']):
        if 'third party' in label.lower():
            return '3P Collection'
        else:
            return '1P Collection'

    return None

def get_answer(label, dimension):
    yes_list = []
    no_list = []
    maybe_list = []
    if dimension == 'Location':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in']

    if dimension == 'Identification':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained']
        no_list = ['does not collect', 'does not receive', 'does not track']
    
    if dimension == 'Targeted Advertising':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does see', 'does do']
        no_list = ['does not collect', 'does not receive', 'does not track', 'does not do']
        
    if dimension == 'Policy Change':
        yes_list = ['are notified', 'are personally notified']
        no_list = ['no notification']
        maybe_list = ['is posted as part of the policy']
    
    if dimension == 'Do Not Track':
        yes_list = ['reads and adheres']
        no_list = ['ignores', 'no statement']
        maybe_list = ['unclear', 'handles']
    
    if dimension == 'Security':
        yes_list = ['encrypted', 'has a privacy or security program/organization', 'security practices', 'security measures']
        no_list = ['not mentioned']
        maybe_list = ['generic security statements', 'specific security measure', 'need-to-know basis']
    
    if dimension == 'Retention':
        yes_list = ['limited', 'stated']
        maybe_list = ['unspecified duration', 'duration not covered']
        no_list = ['indefinitely']
        
    if dimension == 'Action':
        no_list = ['can view', 'can edit', 'can configure', 'can choose', 'can access', 
        'can use', 'can opt out', 'can deactivate', 'can make a choice', 'can export', 'contact']
        yes_list = ['no specified choices', 'can not access']
    
    if dimension == 'Payment':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in']

    if dimension == 'Disclosure':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in']
        
    if dimension == 'Health':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not do']
    
    if dimension == 'Deletion':
        yes_list = ['can delete']
        no_list = ['can not delete']
        
    if dimension == 'Social Media':
        yes_list = ['collects']
        no_list = ['does not collect']

    if dimension == 'Personalization':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not do']
        
    if dimension == 'Contact Info':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not do', 'does not see']
        
    if dimension == 'Activity':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not do', 'does not see']
        
    if dimension == 'Personal Info':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not do', 'does not see']
        maybe_list = ['outside of our label scheme']
        
    if dimension == '3P Analysis' or dimension == '1P Analysis':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not do', 'does not see']
    
    if dimension == '3P Collection' or dimension == '1P Collection':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not do', 'does not see']
    
    if dimension == 'Cookies':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not do', 'does not see']
    
    if any(s in label.lower() for s in yes_list):
        return 'Yes'
    if any(s in label.lower() for s in no_list):
        return 'No'
    if any(s in label.lower() for s in maybe_list):
        return 'Maybe'

    # by default
    return 'Maybe'

def build_dataset(a_file, l_file):
    temp_list = []
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
                    value = attrs[category]['value']
                    selected_text = attrs[category]['selectedText']
                    # cleanup of raw text selection
                    if not value=='not-selected' and not value=='Unspecified' and 'null' not in selected_text:
                        raw_text += ' ' + selected_text

            temp_dict['annotation_id'] = annotation_id
            temp_dict['dimension'] = opp_dimension
            temp_dict['raw_text'] = raw_text

            temp_list.append(temp_dict)

    label_dataset = {}
    with open(l_file) as label_file:
        reader = csv.reader(label_file)
        for row in reader:
            annotation_id = row[0]
            label = row[3]
            label_dataset[annotation_id] = label

    policy_data = []
    
    for row in temp_list:
        raw_text = row['raw_text']
        label = label_dataset[row['annotation_id']]
        dimension = get_dimension(label, row['dimension'])
        
        # exclude datapoints that don't fit into our dimensions
        if not dimension:
            continue
        
        answer = get_answer(label, dimension)
        dim_list.append(dimension)
        policy_data.append([row['raw_text'], label, dimension, answer])

    return policy_data

# Splitting the full dataset into train and test sets
def split_dataset(full_dataset):
    
    raw_text = [row[0] for row in full_dataset]
    labels = [row[1] for row in full_dataset]
    X = raw_text + labels
    y = [row[2] for row in full_dataset] * 2

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4, stratify=y)

    pickle.dump(X_train, open(os.path.join(curr_folder, '../datasets/X_train.p'), 'wb'))
    pickle.dump(X_test, open(os.path.join(curr_folder, '../datasets/X_test.p'), 'wb'))
    pickle.dump(y_train, open(os.path.join(curr_folder, '../datasets/y_train.p'), 'wb'))
    pickle.dump(y_test, open(os.path.join(curr_folder, '../datasets/y_test.p'), 'wb'))

    dim_data = {}
    for dim in set(y):
        dim_data[dim] = {}
        
        dim_rows = [row for row in full_dataset if row[2]==dim]
        raw_text = [row[0] for row in dim_rows]
        labels = [row[1] for row in dim_rows]
        X = raw_text + labels
        y = [row[3] for row in dim_rows] * 2
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4, stratify=y)
        
        dim_data[dim]['X_train'] = X_train
        dim_data[dim]['X_test'] = X_test
        dim_data[dim]['y_train'] = y_train
        dim_data[dim]['y_test'] = y_test
    
    pickle.dump(dim_data, open(os.path.join(curr_folder, '../datasets/dim_data.p'), 'wb'))

def main():
    full_dataset = []

    label_directory = os.path.join(curr_folder, '../OPP-115/pretty_print/')
    annotation_directory = os.path.join(curr_folder, '../OPP-115/annotations/')
    
    """
    build dataset for every single policy in OPP-115
    dataset consists of 4 columns:
    1) raw text from the policy
    2) OPP 115 label
    3) Priv dimension (defined in get_dimension fcn)
    4) Priv answer (Yes/No/Maybe)
    """
    print('Building dataset...')
    for filename in os.listdir(annotation_directory):
        match = re.search('[\d]+_(.+)', filename)
        label_name = match[1]
        l_file = label_directory + label_name
        a_file = annotation_directory + filename
        policy_data = build_dataset(a_file, l_file)
        full_dataset += policy_data

    # Printing the number of samples for each dimension
    # print('Dimension counts:')
    # counts =  [(x, dim_list.count(x)) for x in set(dim_list)]
    # print(counts)

    folder = os.path.join(curr_folder, '../datasets')
    if not os.path.exists(folder):
        print("Making directory: " + folder)
        os.makedirs(folder)

    print('Saving full dataset in full_dataset.csv...')
    with open(os.path.join(curr_folder, '../datasets/full_dataset.csv'), 'w') as f:
        wr = csv.writer(f,delimiter=',')
        for row in full_dataset:
            wr.writerow(row)

    print('Splitting dataset into test and train sets...')
    split_dataset(full_dataset)
    
    print('Done transforming data :)')

if __name__ == "__main__":
    main()