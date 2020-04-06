'''
Script for Python36 or above only because of format string

After execute crawler.py 6 times
Run this script to merge all results into one file
'''

import json
from crawler import CODEJAM_ROUND


RESULT_FILE_NAME = 'all_data_by_rank.json'

def save_to_file(res):
    with open(RESULT_FILE_NAME, 'w') as f:
        # json.dump(res, f, indent=2, sort_keys=True)  # debug only, we'll handle data by pandas
        json.dump(res, f)


d = {}
total = 0
for i in ['200', '50', '10', '5', '1']:
    with open(f'{CODEJAM_ROUND}_{i}.json') as f:
        users = json.loads(f.read())

    for u in users:
        # additional aggregation to make pandas handle data easily
        total_attempts = 0
        for i in u['task_info']:
            total_attempts += i['total_attempts']
        u['total_attempts'] = total_attempts
        d[u['rank']] = u

save_to_file(d)
