import csv

with open('./OPP-115/annotations/105_amazon.com.csv') as amzn:
    reader = csv.reader(amzn, dialect='excel')
    for row in reader:
        print '\n\n'.join(row)