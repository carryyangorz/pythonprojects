import requests
import os
import time
import re
import json

from openpyxl import Workbook
from openpyxl import load_workbook

from time import sleep

from threading import Timer
import threading

num=200
c[i]num=0
headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }

# url='https://plantsservices.sc.egov.usda.gov/api/PlantProfile?symbol=ABAB'
# r=requests.get(url,headers=headers)
# group=re.findall('"Group":"(.*)","RankId',r.text)[0]
# Durations=re.findall('"Durations":(.*?),"GrowthHabits',r.text)[0]
# Durations=Durations.replace(',','\n')
# Durations=Durations.replace('["','')
# Durations=Durations.replace('"]','')
# print(Durations)
# GrowthHabit=re.findall('"GrowthHabits":(.*?),"NativeStatuses',r.text)[0]
# GrowthHabit=GrowthHabit.replace(',','\n')
# GrowthHabit=GrowthHabit.replace('"','')
# GrowthHabit=GrowthHabit.replace('[','')
# GrowthHabit=GrowthHabit.replace(']','')
# print(GrowthHabit)
# GrowthHabit=re.findall('"NativeStatuses":(.*?),"MapCoordinates',r.text)[0]
# reg=re.findall('Region":"(.*?)","Status',GrowthHabit)
# status=re.findall('Status":"(.*?)","Type',GrowthHabit)
# print(len(reg))
# GrowthHabit=''
# for i in range(0,len(reg)):
#     # print(reg[i]+' '+status[i])
#     # print('=====')
#     GrowthHabit+=reg[i]+' '+status[i]+'\n'
# print(GrowthHabit)
keydick={
    "Field": "Symbol",
    "MasterId": 65791,
    "Offset": "",
    "SortBy": "sortSciName",
    "Text": "ABAB"

}
a=requests.post('https://plantsservices.sc.egov.usda.gov/api/PlantProfile/getDownloadDistributionDocumentation',data=keydick)
a=json.loads(a.text)
# print(a['PlantResults'])
b=a['PlantResults'][0]
c=b['PlantsDistributionResults']
wb=Workbook()
ws=wb.active
ls=[]
for i in range(0,len(c)):
# for c[i] in c:
    # print(c[i])
    ls.append(c[i]["Symbol"]+','+c[i]["Country"]+','+c[i]["Country"]+','+c[i]["State"]+','+c[i]["StateFIP"]+','+c[i]["County"]+','+c[i]["CountyFIP"])

print(ls)