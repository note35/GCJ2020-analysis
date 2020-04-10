'''
Script for Python36 or above only because of format string

This is a semi-automated script because the API return sometimes might return broken data
You need to run this script 6 times...
1 query_all() with NUMS_CONSECUTIVE_USERS = 200
5 query_missed() with LAST_NUMS_CONSECUTIVE_USERS = [200, 50, 10, 5] and NUMS_CONSECUTIVE_USERS = [50, 10, 5, 1] respectively
'''
import base64
import json
import re
import ssl
import time
import urllib.request


# Qualification Round
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27
CODEJAM_ROUND = '000000000019fd27'
URL = f'https://codejam.googleapis.com/scoreboard/{CODEJAM_ROUND}/poll?p='
NUMS_CONSECUTIVE_USERS = 50
LAST_NUMS_CONSECUTIVE_USERS = 200
RATE_LIMIT = 0.05
SSL_CONTEXT = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional (Javascript Compatible Base64 decode)

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.
    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)


class RankCrawler:
    def __init__(self, url):
        self.url = url

    def get_payload(self, offset):
        return base64.b64encode(
            ('{"min_rank":' + str(offset) + ',"num_consecutive_users":' + str(NUMS_CONSECUTIVE_USERS) + '}').encode('utf-8')
        ).decode('utf-8')

    def query(self, payload):
        time.sleep(RATE_LIMIT)
        b64resp = urllib.request.urlopen(self.url + payload, context=SSL_CONTEXT).read()
        resp = decode_base64(b64resp).decode('utf-8')
        return json.loads(resp)


def query_missed():
    # In GCJ 2020 - Qual round, few data are broken caused the API unable to return parsable data
    # NUMS_CONSECUTIVE_USERS: 200
    missed = [7401, 8401, 9601, 9801, 10401, 11601, 12001, 12601, 13601, 14401, 14601, 14801, 15401, 19001, 19201, 19401, 20401, 21001, 27201, 28001, 28401, 30601, 31801, 32201, 34401, 35201, 37201, 38001, 38201, 39001, 39801, 40801, 41601]
    # NUMS_CONSECUTIVE_USERS: 50
    # missed = [7501, 8401, 9801, 12051, 12601, 14451, 14601, 14801, 15501, 19001, 19301, 19501, 20401, 27251, 28401, 32251, 34451, 35351, 37301, 38001, 39001, 39101, 39801, 40951]
    # NUMS_CONSECUTIVE_USERS: 10
    # missed = [7526, 8401, 9826, 12051, 12076, 14601, 14826, 15526, 19026, 19501, 20401, 27251, 28426, 32251, 34451, 35376, 37301, 38001, 39026, 39801, 40951]
    # NUMS_CONSECUTIVE_USERS: 5
    # missed = [7541, 8401, 9826, 12081, 14621, 19031, 20406, 27266, 28431, 32271, 34466, 35376, 37301, 38006, 39031, 39821, 40951]
    # NUMS_CONSECUTIVE_USERS: 1 (broken data)
    # missed = [7544, 8401, 9827, 12085, 14624, 19035, 20409, 27270, 28434, 32273, 34470, 35376, 37301, 38010, 39035, 39825, 40953]
    rc = RankCrawler(URL)
    user_res = []
    failed = []
    for offset in missed:
        # eg: NUMS_CONSECUTIVE_USERS = 200 found a failed query
        # then we will check by NUMS_CONSECUTIVE_USERS = 50
        # for i in range(0, 200, 50):
        for i in range(0, LAST_NUMS_CONSECUTIVE_USERS, NUMS_CONSECUTIVE_USERS):
            payload = rc.get_payload(offset+i)
            print(offset+i, payload)
            try:
                resp = rc.query(payload)
            except:
                failed.append(offset+i)
                print(f'failed at offset: {offset+i}')
                continue
            if len(resp['user_scores']) == 0:
                break
            user_res += resp['user_scores']
    print(failed)
    return user_res


def query_all():
    rc = RankCrawler(URL)
    user_res = []
    failed = []
    offset = 1
    while True:
        payload = rc.get_payload(offset)
        print(offset, payload)
        try:
            resp = rc.query(payload)
        except:
            failed.append(offset)
            print(f'failed at offset: {offset}')
            continue
        if len(resp['user_scores']) == 0:
            break
        user_res += resp['user_scores']
        offset += 200
        break
    print(failed)
    return user_res


def save_to_file(res, fn):
    with open(fn, 'w') as f:
        json.dump(res, f)


if __name__ == '__main__':
    save_to_file(query_all(), f'{CODEJAM_ROUND}_{NUMS_CONSECUTIVE_USERS}.json')
    # save_to_file(query_missed(), f'{CODEJAM_ROUND}_{NUMS_CONSECUTIVE_USERS}.json')
