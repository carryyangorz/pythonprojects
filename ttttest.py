import re
import requests
a='https://bs.plantnet.org/image/o/84a53a61f21b0d10f611e31e4bf20821d95144cb'
b=re.findall('/o/(.*)',a)
# print(b)
headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
c=3
d=4
# print(max(c,d))

name='Zea mays'
url='https://api.plantnet.org/v1/projects/namerica/species?pageSize=50&page=0&lang=en&search='+name+'&sortBy=images_count&sortOrder=desc'
picurl='https://bs.plantnet.org/image/o/cef981f51656ee660516a56a5969f4eb50c9dbc9'
newurl='https://bs.plantnet.org/image/o/68d3b5186346d3b4df5c1d1664b03d55f5dce770'
r=requests.get(newurl,headers=headers)
r.raise_for_status()
f=open('test.jpg','wb')
f.write(r.content)
f.close()

# r=requests.get(picurl,headers==headers)
# r.raise_for_status()
# f=open('test.jpg','wb')
# f.write(r.content)
# f.close()