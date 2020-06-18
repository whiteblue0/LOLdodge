from decouple import config
import requests
import csv


def getMatches(res):
    try:
        matches = res.get('matches')
    except KeyError:
        print(res)
        if res.get("status").get('status_code'):
            return res.get("status").get('status_code')

    return matches


host = 'https://kr.api.riotgames.com'
API_KEY = config('API_KEY')
quetype = 420   # 420: 솔랭 코드번호

limit_sec = 0
limit_min = 0

# print(ACCOUNT_ID)
encryptedAccountId = 'v_KpcC3k3Hq-Bo4vKXZVYPTC8GP5lMWSXZFLwluOmtY'
url = f'{host}/lol/match/v4/matchlists/by-account/{encryptedAccountId}?queue={quetype}&api_key={API_KEY}'
print(url)
res = requests.get(url).json()
matches = res.get('matches')
print(res)
init = True
data = dict()
if matches:
    with open('./data/my_matches.csv', 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['gameId', "champion", "lane"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if init:
            writer.writeheader()
        for match in matches:
            data['gameId'] = match.get('gameId')
            data['champion'] = match.get('champion')
            data['lane'] = match.get('lane')
            writer.writerow(data)
