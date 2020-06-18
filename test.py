# from decouple import config
# import requests
# import csv
# import time

# matchid_list = [1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10]

# init = False
# data = dict()
# with open('./data/test.csv', 'a', newline='', encoding='utf-8') as f:
#     fieldnames = ['matchId']
#     writer = csv.DictWriter(f, fieldnames=fieldnames)
#     if init:
#         writer.writeheader()
#     for matchId in matchid_list:
#         data["matchId"] = matchId
#         writer.writerow(data)
