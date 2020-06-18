from decouple import config
import requests
import csv
from time import sleep
from time import time as timer

host = 'https://kr.api.riotgames.com'
API_KEY = config('API_KEY')

# setting
queue = 'RANKED_SOLO_5x5'
tier = 'IV'
divison = 'DIAMOND'
init = False
page = 98

while page < 101:
    set_time = timer()
    que_url = f'{host}/lol/league/v4/entries/{queue}/{divison}/{tier}?page={page}&api_key={API_KEY}'

    res = requests.get(que_url)
    print("page:", page)
    summoner_list = res.json()
    # print(summoner_list)
    # summoner_name_list = []
    # for i in range(len(summoner_list)):
    #     name = summoner_list[i].get('summonerName')
    #     if name in summoner_name_list:
    #         continue
    #     else:
    # summoner_name_list.append(name)

    # get summoner list
    user_data = dict()

    with open('./data/id_list.csv', 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['accountId', 'summonerName', 'tier', 'rank']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if init:
            writer.writeheader()
        minstack = 0
        secstack = 0
        for i in range(len(summoner_list)):

            # make delay
            # max 20 request per 1 second
            # secstack += 1
            # if secstack == 15:
            #     sleep(20)
            #     secstack = 0
            # sleep(1)
            # max 100 request per 120 second
            minstack += 1
            if minstack == 140:
                sleep(10)
                minstack = 0

            account_res = requests.get(
                f"{host}/lol/summoner/v4/summoners/by-name/{summoner_list[i].get('summonerName')}?api_key={API_KEY}").json()

            user_data['accountId'] = account_res.get('accountId')
            user_data['summonerName'] = summoner_list[i].get('summonerName')
            user_data['tier'] = summoner_list[i].get('tier')
            user_data['rank'] = summoner_list[i].get('rank')

            # valid check
            if user_data['accountId'] == None:
                continue
            # if user_data['accountId'] in summoner_name_list:
            #     continue

            writer.writerow(user_data)
            print(account_res)
            print(user_data)
            print()
    page += 1
    endtime = timer()
    print(endtime-set_time)
