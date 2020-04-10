'''
Script for Python36 or above only because of format string

Step1: Run rank_crawler.py and data_merger.py first to get all_data_by_rank.json 
Step2: Copy all_data_by_rank.json to all_data_with_lang_by_rank.json

[Caution]
- This script takes more than 2 days to query 40000+ times to the API
- You probably need to modify it to run by multiple process to improve the efficiency
- Do NOT interrupt the process when it's writing data to file
'''
import base64
import json
import re
import ssl
import time
import urllib.request

from rank_crawler import CODEJAM_ROUND, decode_base64, save_to_file


URL = f'https://codejam.googleapis.com/attempts/{CODEJAM_ROUND}/poll?p='
RATE_LIMIT = 0.05
SSL_CONTEXT = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
RESULT_FILE_NAME = 'ttt.json'
SAVE_PER_QUERY = 10  # since we need to query api 40000 times, it's better to keep saving result to file


class LangCrawler:
    def __init__(self, url):
        self.url = url

    def get_payload(self, nickname):
        return base64.b64encode(
            ('{"nickname":"' + nickname + '","include_non_final_results":false}').encode('utf-8')
        ).decode('utf-8')

    def query(self, payload):
        time.sleep(RATE_LIMIT)
        b64resp = urllib.request.urlopen(self.url + payload, context=SSL_CONTEXT).read()
        sb64resp = b64resp.split(b'-')
        languages = []
        for item in sb64resp:
            try:
                ditem = decode_base64(item).decode('utf-8')
            except:
                # Note that since the API return is often undecodable, we can only get decodable part of return
                # Example: https://codingcompetitions.withgoogle.com/codejam/submissions/000000000019fd27/V29ua28
                continue
            # the api returns incomplete json, we can only use regex to parse the language result...
            groups = re.match(r'.*src_language__str\":\"(.*)\",\"task_id.*', ditem)
            if groups:
                languages.append(groups[1])
        return languages


lc = LangCrawler(URL)
processed = set()
# Known problematic API key
failed = {'66', '70', '93', '156', '255', '328', '537', '552', '817', '863', '877', '902', '929', '1410', '1647', '1952', '1954', '2174', '2684', '3082', '3912', '4128', '4699', '4757', '4889', '4895', '5460', '5498', '5775', '5989', '6121', '6180', '6570', '6722', '6777', '6793', '6864', '7445', '7564', '7728', '7894', '8900', '9152', '9689', '10503', '11407', '11662', '11884', '12073', '12137', '12423', '12514', '12649', '12662', '12790', '13180', '13778', '13800', '13891', '14479', '14498', '15677', '15987', '16497', '17180', '17394', '17402', '17532', '18085', '18096', '18244', '18459', '19190', '19236', '19368', '19475', '19511', '19707', '19870', '20111', '20464', '20741', '20902', '21110', '22326', '22446', '22557', '22669', '22732', '23167', '23276', '23875', '24057', '24246', '24384', '24386', '24824', '25279', '25644', '26216', '26306', '26385', '26599', '26824', '26953', '26959', '26961', '27067', '27069', '27106', '27329', '27473', '27875', '28102', '28128', '28210', '28300', '29116', '29406', '29560', '30312', '30653', '30742', '31100', '31324', '31791', '32052', '32617', '33655', '34177', '34383', '34444', '34902', '36447', '38603', '38731', '39252', '39605', '40005', '40061', '40185', '40223'}
while True:
    # initialize the counter and reload the file
    cnt = 0
    if cnt % SAVE_PER_QUERY == 0:
        with open(RESULT_FILE_NAME, 'rt') as f:
            all_data = json.loads(f.read())

    # it's inefficient but acceptable to loop entire dict everytime
    has_query = False
    for k, v in all_data.items():
        if k in failed or k in processed or 'languages' in all_data[k]:
            processed.add(k)
            continue
        try:
            # only care distinct value
            all_data[k]['languages'] = list(set(lc.query(lc.get_payload(v['displayname']))))
            print(k, v['displayname'], all_data[k]['languages'])

            cnt += 1
            # if there's SAVE_PER_QUERY queries, break
            if cnt % SAVE_PER_QUERY == 0:
                break
            has_query = True
        except:
            print(f'failed to query: {k}')
            failed.add(k)
        # last item
        if int(k) == 40698:
            has_query = False
            break


    # if there's SAVE_PER_QUERY queries, save result to file
    if has_query is False or cnt % SAVE_PER_QUERY == 0:
        save_to_file(all_data, RESULT_FILE_NAME)

    # if there's no query happen, break
    if has_query is False:
        break
