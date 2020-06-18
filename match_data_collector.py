from decouple import config
import requests
import csv

host = 'https://kr.api.riotgames.com'
API_KEY = config('API_KEY')

match_list = []
with open('./data/my_matches.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        gameId = row['gameId']
        champion = row['champion']
        lane = row['lane']
        match_list.append(gameId)

team1 = dict()
team2 = dict()
isWrite = []
for game_id in match_list:
    url = f'{host}/lol/match/v4/matchlists/matches/{game_id}?api_key={API_KEY}'
    res = requests.get(url).json()
    version = res.get('gameVersion')
    teams = res.get('teams')
    data1 = teams[0]
    data2 = teams[1]
    team1['win'] = data1.get("win")
    temp = []
    for champ in data1.get("bans"):

    team1['bans'] = data1.get("bans")
    team1[]
