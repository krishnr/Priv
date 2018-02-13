import os
import csv

directory = '../OPP-115/pretty_print_uniquified/'

labels = []

for filename in os.listdir(directory):
    with open(directory + filename) as label_file:
        reader = csv.reader(label_file)
        for row in reader:
            labels.append(row[0])

labels = list(set(labels))

with open('../labels.csv', 'w') as f:
    wr = csv.writer(f, delimiter='\n')
    wr.writerow(labels)