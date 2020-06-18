from decouple import config
import requests
import csv
import time


def getMatches(res):
    try:
        matches = res['matches']
    except KeyError:
        print(res)
        if res.get("status").get('status_code'):
            return res.get("status").get('status_code')
        else:
            time.sleep(600)
            getMatches(res)

    return matches


host = 'https://kr.api.riotgames.com'
API_KEY = config('API_KEY')


quetype = 420   # 420: 솔랭 코드번호
id_list = []
with open('./data/id_list.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        accountId = row['accountId']
        id_list.append(accountId)

matchid_list = []
limit_sec = 0
limit_min = 0
stack = 0
start_time = time.time()
id_index = 19733
while id_index >= 0:
    # for i in range(len(id_list)):
    print(f'{id_index}', end="")
    encryptedAccountId = id_list[id_index-1]
    url = f'{host}/lol/match/v4/matchlists/by-account/{encryptedAccountId}?queue={quetype}&api_key={API_KEY}'
    res = requests.get(url).json()

    matches = getMatches(res)
    if matches == 404:
        id_index += 1
        continue
    elif type(matches) == int:
        print(f"{id_index}부터 다시 시작하세요")
        break

    for match in matches:
        match_id = match['gameId']
        # print(match_id, end=" ")
        if match_id not in matchid_list:
            matchid_list.append(match_id)
    print()
    # api request limit: 20 per 1 second, 100 per 120 second
    limit_sec += 1
    limit_min += 1
    if limit_sec == 15:
        limit_sec = 0
        time.sleep(2)
    if limit_min == 80:
        limit_min = 0
        time.sleep(150)

    id_index += 1
    # if id_index == (len(id_list) - 1):
    #     break
    # if stack == 98:
    #     time.sleep(25)

end_time = time.time()

init = False
data = dict()
with open('./data/match_id.csv', 'a', newline='', encoding='utf-8') as f:
    fieldnames = ['matchId']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if init:
        writer.writeheader()
    for matchId in matchid_list:
        data['matchId'] = matchId
        writer.writerow(data)
