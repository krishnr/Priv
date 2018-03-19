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
    - Opt Out
    - Request
    - Location
    - Payment
    - Disclosure
    - Activity
    - Deletion
    - Social Media
    - Personalization
    - Contact Info
    - Analysis
    - 3P Sharing
    - Collection
    - Cookies
    - Log Files
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

    
    if any(s in label.lower() for s in ['request a list', 'request access', 'request a description', 'request a record', 'request a copy', 'request a notice']):
        return 'Request'

    if any(s in label.lower() for s in ['targeted ad', 'targeting', 'targeted marketing', 'target ad', 'tailored ad', 'tailor offers', 'tailor ad']) \
        or all(s in label.lower() for s in ['ad', 'target']):
        return 'Targeted Advertising'
    
    if dimension == 'Policy Change':
        return 'Policy Change'

    if all(s in label.lower() for s in ['respond', 'do not track']) \
        or dimension == 'Do Not Track':
        return 'Do Not Track'
    
    if any(s in label.lower() for s in ['encrypt', 'ssl connection', 'secure socket layers']):
        return 'Security'

    if dimension == 'Data Retention' or any(s in label.lower() for s in ['is retained', 'retain indefinitely']):
        return 'Retention'
    
    if any(s in label.lower() for s in ['keep some data', 'comprehensive removal', 'removal of information', 'retaining some residual']):
        return 'Deletion'

    if any(s in label.lower() for s in ['opt out', 'privacy settings', 'configuration settings']):
        return 'Opt Out'

    if any(s in label.lower() for s in ['geographic location', 'location information', 'physical location', 'location data', 'current location']):
        return 'Location'

    if any(s in label.lower() for s in ['financial information', 'payment information', 'credit card information']):
        return 'Payment'
    
    if any(s in label.lower() for s in ['good faith', 'subpoena', 'court order', \
        'government demand', 'law enforcement', 'search warrant', 'legal action', \
        'compelled by', 'legal request', 'legal process', 'law-enforcement']):
        return 'Disclosure'

    if any(s in label.lower() for s in ['before coming', 'before our', 'referring',\
        'exit pages', 'previous website', 'you came from']):
        return 'Activity'
    
    if any(s in label.lower() for s in ['social media', 'social network ', \
        'via facebook', 'via your facebook', 'like facebook', \
        'third party social networking', 'third-party social networking']):
        return 'Social Media'
    
    if any(s in label.lower() for s in ['ip address', 'device id']):
        return 'Identification'
    
    if any(s in label.lower() for s in ['personalization', 'customization', \
        'personalize and enhance', 'customize and enhance', 'tailored to your interests' \
        'tailored content', 'tailored to you', 'tailor your experience']):
        return 'Personalization'
    
    if any(s in label.lower() for s in ['log file', ' logs ', 'log information', 'log certain', 'complete log']):
        return 'Log Files'

    if any(s in label.lower() for s in ['collects your contact info', 'collect your contact info', 'receive your contact info', 'use of contact info']):
        return 'Contact Info'

    if any(s in label.lower() for s in ['cookies', 'web beacons', 'pixel tag']):
        return 'Cookies'

    if any(s in label.lower() for s in ['demographic','analytics', 'research', 'aggregated', 'anonymized']):
        return 'Analysis'

    if any(s in label.lower() for s in ['named third party', 'unnamed third party', 'unspecified third party', 'named service']):
        return '3P Sharing'

    if any(s in label.lower() for s in ['identifiable', 'profile information', 'personal information', 'collects your user profile']):
        return 'Collection'

    return None


def get_answer(label, dimension):
    yes_list = []
    no_list = []
    maybe_list = []
    if dimension == 'Location':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'can determine', 'use your device', 'using your current location', 'transmits location']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in']    

    if dimension == 'Identification':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained', 'use IP', ]
        no_list = ['does not collect', 'does not receive', 'does not track']
    
    if dimension == 'Targeted Advertising':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does see', 'does do', 'we collect', 'may use', 'displays targeted']
        no_list = ['does not collect', 'does not receive', 'does not track', 'does not do', 'do not knowingly collect']
        
    if dimension == 'Policy Change':
        no_list = ['are notified', 'are personally notified']
        yes_list = ['no notification']
        maybe_list = ['is posted as part of the policy']
    
    if dimension == 'Do Not Track':
        no_list = ['reads and adheres']
        yes_list = ['ignores', 'no statement']
        maybe_list = ['unclear', 'handles']
    
    if dimension == 'Security':
        no_list = ['encrypted', 'adequate security and encryption', 'we use ssl encryption', 'encrypts transmission']
        yes_list = ['not mentioned']
        maybe_list = ['generic security statements', 'specific security measure', 'need-to-know basis']
    
    if dimension == 'Retention':
        no_list = ['limited', 'stated']
        maybe_list = ['unspecified duration', 'duration not covered']
        yes_list = ['indefinitely', 'as long as necessary']
        
    if dimension == 'Opt Out':
        no_list = ['can view', 'can edit', 'can configure', 'can choose', 'can access', 
        'can use', 'can opt out', 'can deactivate', 'can make a choice', 'can export', 
        'contact', 'send a letter', 'may opt out']
        yes_list = ['no specified choices', 'can not access']
    
    if dimension == 'Request':
        no_list = []
        yes_list = ['may request', 'can request', 'contact us', 'request access', 'request a copy', 'permits','may also request']
    
    if dimension == 'Payment':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'be shared']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not handle', 'does not store', 'does not maintain']

    if dimension == 'Disclosure':
        yes_list = ['without a subpoena', 'without first obtaining your permission', 'without notifying you', 'without providing notice', 'without your permission', 'without limitation']
        no_list = []
        
    if dimension == '3P Sharing':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is accessible']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not do']
    
    if dimension == 'Log Files':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained','collected log information']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not do']

    if dimension == 'Deletion':
        no_list = ['can delete']
        yes_list = ['can not delete', 'some residual information','may continue to keep some data', 'decline requests for removal']
        
    if dimension == 'Social Media':
        yes_list = ['collects', 'does collect', 'does receive', 'does track']
        no_list = ['does not collect', 'does not receive', 'does not track', 'do not record']

    if dimension == 'Personalization':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained', 'also personalize']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not do', 'not use']
        
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
        
    if dimension == 'Analysis':
        yes_list = ['collects', 'does collect', 'does receive', 'does track', 'does do', 'does see', 'is retained']
        no_list = ['does not collect', 'does not receive', 'does not track', 'can opt in', 'does not do', 'does not see']
    
    if dimension == 'Collection':
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
        dimension = get_dimension(raw_text + label, row['dimension'])
        
        # exclude datapoints that don't fit into our dimensions
        if not dimension:
            continue
        
        answer = get_answer(raw_text + label, dimension)
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

    pickle.dump(X_train, open(os.path.join(curr_folder, '../../datasets/X_train.p'), 'wb'))
    pickle.dump(X_test, open(os.path.join(curr_folder, '../../datasets/X_test.p'), 'wb'))
    pickle.dump(y_train, open(os.path.join(curr_folder, '../../datasets/y_train.p'), 'wb'))
    pickle.dump(y_test, open(os.path.join(curr_folder, '../../datasets/y_test.p'), 'wb'))

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
    
    pickle.dump(dim_data, open(os.path.join(curr_folder, '../../datasets/dim_data.p'), 'wb'))


def main():
    full_dataset = []

    label_directory = os.path.join(curr_folder, '../../OPP-115/pretty_print/')
    annotation_directory = os.path.join(curr_folder, '../../OPP-115/annotations/')
    
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
        label_name = match.group(1)
        l_file = label_directory + label_name
        a_file = annotation_directory + filename
        policy_data = build_dataset(a_file, l_file)
        full_dataset += policy_data

    # Printing the number of samples for each dimension
    # print('Dimension counts:')
    # counts =  [(x, dim_list.count(x)) for x in set(dim_list)]
    # print(counts)

    folder = os.path.join(curr_folder, '../../datasets')
    if not os.path.exists(folder):
        print("Making directory: " + folder)
        os.makedirs(folder)

    print('Saving full dataset in full_dataset.csv...')
    with open(os.path.join(curr_folder, '../../datasets/full_dataset.csv'), 'w') as f:
        wr = csv.writer(f,delimiter=',')
        for row in full_dataset:
            wr.writerow(row)

    print('Splitting dataset into test and train sets...')
    split_dataset(full_dataset)
    
    print('Done transforming data :)')


if __name__ == "__main__":
    main()
