# Caden Oslund
# CPT_S 315 Final Project
# Item-Item Database for Water Quality Monitoring

from apyori import apriori
import csv
import pandas as pd

indentifiers = []
values = []

# Reads the data file and splits it into values and identifiers
with open('converteddata.csv', 'r') as datafile:
    reader = csv.reader(datafile)
    for row in reader:
        indentifiers.append(row[0])
        values.append(int(row[1]))

buckets = []

# Adds stations to bucket if they are within 100 of each other
for i in range(len(indentifiers)):
    bucket = [indentifiers[i]]

    for j in range(len(indentifiers)):
        if indentifiers[i] != indentifiers[j] and values[i] - values[j] <= 100:
            bucket.append(indentifiers[j])
    
    buckets.append(bucket)

largest = 0

# Finds the size of the largest bucket
for bucket in buckets:
    if len(bucket) > largest:
        largest = len(bucket)

# Pads the other buckets to be equal in size
for bucket in buckets:
    while len(bucket) < largest:
        bucket.append('')

# Writes the bucketed data to a file
with open('bucketeddata.csv', 'w') as csvFile:
    csvWriter = csv.writer(csvFile, delimiter=',', lineterminator='\n')
    csvWriter.writerows(buckets)

# Setting up for apriori
data = pd.read_csv('bucketeddata.csv', header = None)
data.fillna("", inplace=True)

# Sets up the data to be run through the algorithm
records = []
rows = data.shape[0]
columns = data.shape[1]

for i in range(rows):
    records.append([str(data.values[i, j]) for j in range(columns) if str(data.values[i,j]) != ""])

# Chosen through testing to get a reasonable amount of results, getting a large result while only keeping accurate groupings
support = 45/rows

# Runs Apriori algorithm on the data
rules = apriori(records, min_support=support, min_confidence=0.9, min_lift=3, max_length=3)

# Filters the results
results = list(rules)
results = list(filter(lambda x: len(x.items) > 2, results))
results.sort(key=lambda x: (-x[2][0][2], [i for i in x[0]][0], [i for i in x[0]][1], [i for i in x[0]][2]))

data = ""

# Processes and prints output
for i in results:
    result = i[0]
    items = [x for x in result]

    print("Rule: " + items[0] + " -> " + items[1] + " -> " + items[2])
    print("Support: " + str(i[1]))
    print("Confidence: " + str(i[2][0][2]))
    print("Lift: " + str(i[2][0][3]))
    print("-----------------------------")

    if data != "":
        data += '\n'
    data += items[0] + " " + items[1] + " " + items[2] + " " + str(i[2][0][2])

# Saved output
with open('output.txt', 'w') as saveFile:
    saveFile.write(data)