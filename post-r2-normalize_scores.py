"""
This file takes the csv file containing score for all the papers as input and output the HotCRP bulk update csv file as outputs.
The score average algorithm is borrowed from the script from PLDI 2020.
"""

import itertools
from collections import defaultdict
import csv
import numpy as np
from utils import read_csv_to_dict, save_dict_to_csv

scores_file = 'post_round2/pldi2022-scores.csv'

# score_char_to_number = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
min_reviews = 3

def load_scores(filename):
    res = defaultdict(list)
    paper_to_title = defaultdict(str)
    paper_to_decision = defaultdict(str)
    email_to_name = defaultdict(str)
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            paper_id = int(row[0])
            title = row[1]
            decision = row[2]
            name = row[4]
            email = row[5]
            score = int(row[6])
            res[paper_id].append((email, score))

            if paper_id not in paper_to_title:
                paper_to_title[paper_id] = title
            if email not in email_to_name:
                email_to_name[email] = name
            if paper_id not in paper_to_decision:
                paper_to_decision[paper_id] = decision
    return res, paper_to_title, email_to_name, paper_to_decision

def get_average_score(papers_to_raw_scores):
    all_scores = list(itertools.chain.from_iterable([[s[1] for s in scores_per_rev] for scores_per_rev in papers_to_raw_scores.values()]))
    avg = np.mean(all_scores)

    return avg

def get_per_user_avg(papers_to_raw_scores):
    rev_to_scores = defaultdict(list)
    for email, score in itertools.chain.from_iterable(papers_to_raw_scores.values()):
        rev_to_scores[email].append(score)
    result = {e: np.mean(scores) for e, scores in rev_to_scores.items() if len(scores) >= min_reviews}
    return result


def normalize_paper_scores(avg_score, papers_to_raw_scores, per_user_avg):
    per_user_avg = defaultdict(lambda: avg_score, per_user_avg)
    result = {}
    for paper_id, emails_and_scores in papers_to_raw_scores.items():
        scores = [(s - per_user_avg[e] + avg_score) for e, s in emails_and_scores]
        result[paper_id] = np.mean(scores)
    return result

if __name__ == '__main__':
    papers_to_raw_scores, paper_to_title, email_to_name, paper_to_decision = load_scores(scores_file)
    avg_score = get_average_score(papers_to_raw_scores)
    print(f'Average score: {avg_score:.3f}')
    print('(Strong Accept=5, Strong Reject=1, so higher is better)')
    per_user_avg = get_per_user_avg(papers_to_raw_scores)

    print()
    print('Reviewers ranked by their average score: ')
    reviewer_avg_score = []
    for e, user_avg_score in sorted(per_user_avg.items(), key=lambda item: item[1]):
        reviewer_avg_score.append({'Email': e, 'Name': email_to_name[e], 'Avg Score': f'{user_avg_score:.3f}'})
    save_dict_to_csv('reviewers_avg_scores.csv', reviewer_avg_score)
    

    print()
    paper_to_normalized_score = normalize_paper_scores(avg_score, papers_to_raw_scores, per_user_avg)
    print('Ranked normalized papers:')
    normalized_scores = []
    for paper_id, normalized_score in sorted(paper_to_normalized_score.items(), key=lambda item: item[1]):
        normalized_scores.append({'ID': paper_id, "Title": paper_to_title[paper_id], 'Normalized Score': f'{normalized_score:.3f}', 'Original Score': f'{np.mean([p[1] for p in papers_to_raw_scores[paper_id]]):.3f}', 'Decision': paper_to_decision[paper_id]})
    save_dict_to_csv('normalized_scores.csv', normalized_scores)

    print()
    print("Produce a sheet for each area chair")
    pc_assignment = read_csv_to_dict('post_round2/pldi2022-pcassignments.csv')
    meta_reviewers_to_paper_id = defaultdict(list)
    for entry in pc_assignment:
        if entry['action'] == 'metareview':
            meta_reviewers_to_paper_id[entry['email']].append(entry['paper'])
    
    print(meta_reviewers_to_paper_id)
    meta_reviewers_to_paper_scores = defaultdict(list)
    for email, paper_ids in meta_reviewers_to_paper_id.items():
        for paper_id in paper_ids:
            paper_id = int(paper_id)
            meta_reviewers_to_paper_scores[email].append({'ID': paper_id, 'Title': paper_to_title[paper_id], 'Normalized score': f'{paper_to_normalized_score[paper_id]:.3f}', 'Original score': f'{np.mean([p[1] for p in papers_to_raw_scores[paper_id]]):.3f}'})
        save_dict_to_csv('{}_normalized_scores.csv'.format(email), meta_reviewers_to_paper_scores[email])

    print()
    print("Generate the bulk update files")
    tag_updates = []
    for entry in normalized_scores:
        tag_updates.append({'paper': entry['ID'], 'tag': 'avg', 'value': entry['Original Score']})
        tag_updates.append({'paper': entry['ID'], 'tag': 'normal', 'value': entry['Normalized Score']})
    save_dict_to_csv('score_tag_bulk_update.csv', tag_updates)
