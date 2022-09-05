"""
This file takes in the TPMS assignment and outputs the csv file to used for bulk edit in HotCRP
"""

from utils import read_csv_to_dict, save_dict_to_csv

tmps_assignment = read_csv_to_dict('pldi22_round2_assignments.csv')
round = 2

hotcrp_assignment = []

if round == 2:
    for entry in tmps_assignment:
        hotcrp_assignment.append({'paper': entry['paper ID'], 'action': 'primary', 'email': entry['reviewer Email'], 'round': 'R2'})

save_dict_to_csv('pldi22_round2_assignments_hotcrp.csv', hotcrp_assignment)