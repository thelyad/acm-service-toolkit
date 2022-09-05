from csv import DictReader
import os
from typing import List
from utils import *
from utils import read_csv_to_dict
from utils import save_dict_to_csv

"""
This scripts takes in the csv files outputed by HotCrp and generates the input to send to TPMS
Inputs required to run this script:
    - pldi2022-pcinfo.csv: a csv file containing first, last, email, affilation, country
    - papers: a folder containing pdfs with names like pldi2022-paperXXX.pdf
    - pldi2022-pcconflicts.csv: a csv file containing paper_id, title, first, last, email, conflict_type
    - pldi2022-allprefs.csv: paper_id, title, first, last, email, preference, expertise,topic score, conflict
"""

round_2 = True

# reviewers.csv: first, last, email, affilation, country => email,first,last
pcinfo: List[DictReader] = read_csv_to_dict('pldi2022-pcinfo.csv')
filtered_pc_info = []

for reviewer in pcinfo:
    filtered_pc_info.append({'email': reviewer['email'], 'first': reviewer['first'], 'last': reviewer['last']})

save_dict_to_csv('pcinfo_new.csv', filtered_pc_info)

# papers: pldi2022-paperXXX.pdf => paperXXX.pdf
old_papers_folder = 'pldi2022-papers'
new_papers_folder = 'papers_new'
if not os.path.exists(new_papers_folder):
    os.mkdir(new_papers_folder)
for filename in os.listdir(old_papers_folder):
    if filename.endswith('.pdf'):
        filename_new = filename.split('-')[1]
        os.system('cp {}/{} {}/{}'.format(old_papers_folder, filename, new_papers_folder, filename_new))


# coi paper_id, title, first, last, email, conflict_type => paper_id, reviewer_email
coi_info : List[DictReader] = read_csv_to_dict('pldi2022-pcconflicts.csv')
filtered_coi_info = []

for submission in coi_info:
    filtered_coi_info.append({'paper_id': submission['paper'], 'email': submission['email']})

# for round 2: for each submission, also need to add the reviewer's email to the coi csv
if round_2:
    pc_assign_info : List[DictReader] = read_csv_to_dict('pldi2022-pcassignments.csv')

    for submission in pc_assign_info:
        if submission['round'] != 'R1':
            continue
        filtered_coi_info.append({'paper_id': submission['paper'], 'email': submission['email']})

save_dict_to_csv('pcconflicts_new.csv', filtered_coi_info)

# bids.csv: paper_id, title, first, last, email, preference, expertise,topic score, conflict => email, paper_id, score
all_prefs : List[DictReader] = read_csv_to_dict('pldi2022-allprefs.csv')
filtered_all_prefs = []

for pref in all_prefs:
    if pref['preference'] == '':
        continue
    filtered_all_prefs.append({'email': pref['email'], 'paper_id': pref['paper'], 'score': pref['preference']})

save_dict_to_csv('allprefs_new.csv', filtered_all_prefs)

