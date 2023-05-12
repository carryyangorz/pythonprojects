import re
import requests
import json
import ast
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
url='https://api.inaturalist.org/v1/observations/species_counts?verifiable=true&spam=false&place_id=1&iconic_taxa%5B%5D=Plantae&locale=zh-CN&page=213&per_page=100'
r=requests.get(url,headers=headers)
aaa=re.findall('("count":.*?)}}',r.text)
print(len(aaa))

