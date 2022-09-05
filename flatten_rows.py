"""
Given a csv that contains a column where each row looks like "A; B; C", outputs a csv contains a column where "A; B; C" is split to same row. 
"""

import csv

input_f_name = 'names.csv'
output_f_name = 'names_new.csv'
column = 'Research area'

entry = []

with open(input_f_name, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        entry.extend([r.strip()[0].upper() + r.strip()[1:].lower() for r in row[column].strip().split(';') if len(r) > 1])

print(entry)

with open(output_f_name, 'w') as csvfile:
    for e in entry:
        csvfile.write("{}\n".format(e))