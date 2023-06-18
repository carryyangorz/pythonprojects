import re
import requests
import os
from pyquery import PyQuery as pq

# print(b)
headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }

# print(max(c,d))
def download_one_v2(data):
    id=data[0]
    name=data[1]
    url='https://www.gbif.org/occurrence/'+id

    url1='https://www.gbif.org/api/template/occurrence/'+id+'?v=1686130320019'
    r=requests.get(url1,headers=headers)
    doc=pq(r.text)
    a=re.findall('a href="(.*?)" class="imgContainer"',r.text)[0]
    a=re.findall('media/(.*)',a)[0]
    print(a)
    picname=name+'_'+a+'.jpg'
    picurl='https://api.gbif.org/v1/image/cache/occurrence/'+id+'/media/'+a
    data1dic={
        'creator':' ',
        'publisher':' ',
        'license':' ',
        'references':' ',
        'created':' ',
        'rightsHolder':' ',
        'identifier':' ',
        'Suggested citation':' '
        }
    data2dic={
        'Continent':' ',
        'Coordinate uncertainty in metres':' ',
        'Country or area':' ',
        'Country code':' ',
        'Decimal latitude':' ',
        'Decimal longitude':' ',
        'Geodetic datum':' ',
        'State province':' ',
        'Verbatim locality':' '
        }
    datals1=[]
    datals2=[]
    b=doc('figcaption.card__content')
    it=b('div').items()
    for item in it:
        # print(item)
        if item('dt').text()=='creator':
            data1dic[item('dt').text()]=item('span').text()
            continue
        if item('dt').text()=='publisher':
            data1dic[item('dt').text()]=item('span').text()
            continue
        if item('dt').text()=='license':
            data1dic[item('dt').text()]=item('a').attr('href')
            continue
        if item('dt').text()=='references':
            data1dic[item('dt').text()]=item('a').attr('href')
            continue
        if item('dt').text()=='created':
            data1dic[item('dt').text()]=item('span').text()
            continue
        if item('dt').text()=='rightsHolder':
            data1dic[item('dt').text()]=item('span').text()
            continue
        if item('dt').text()=='identifier':
            data1dic[item('dt').text()]=item('a').attr('href')
            continue
        if item('dt').text()=='Suggested citation':
            Suggested=item.text()
            ls=Suggested.split('\n')
            ls.remove(ls[0])
            Suggested=''
            for item in ls:
                Suggested+=item;
            data1dic['Suggested citation']=Suggested
            continue

    print(data1dic)
    b=doc('div.term-block__terms')
    t=b('tr').items()
    for item in t:
        c=item('td').items()
        for ee in c:
                # print(ee.text())
                if ee.text()=='Continent':
                        data2dic['Continent'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Coordinate uncertainty in metres':
                        data2dic['Coordinate uncertainty in metres'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Country or area':
                        data2dic['Country or area'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Country code':
                        data2dic['Country code'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Decimal latitude':
                        data2dic['Decimal latitude'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Decimal longitude':
                        data2dic['Decimal longitude'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Geodetic datum':
                        data2dic['Geodetic datum'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='State province':
                        data2dic['State province'] = (list(item('span').items()))[0].text()
                        continue
                if ee.text()=='Verbatim locality':
                        data2dic['Verbatim locality'] = (list(item('span').items()))[0].text()
                        continue
    print(data2dic)
    if os.path.exists(name+"//"+picname):
        print(name+"//"+picname+'  already exists')
        return
    
    for item in data2dic.values():
         datals2.append(item)
    for item in data1dic.values():
         datals1.append(item)
    r=requests.get(picurl,headers=headers)
    f=open(name+"//"+picname,'wb')
    f.write(r.content)
    f.close()
    f=open(name+'//'+name+'_'+a+'.txt','a',encoding='UTF-8')
    f.write(id+'\n'+url+'\n'+a+'\n')
    for item in datals1:
         f.write(item+'\n')
    for item in datals2:
         f.write(item+'\n')
    f.close()
    print(name +'  +1')


if __name__ == "__main__":
    data=['4011558234','Vigna marina']
    download_one_v2(data)
