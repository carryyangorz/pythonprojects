import json
import random
import re
import time
from pymongo import MongoClient
import requests
from lxml import html

class MeituanSpider():
    def __init__(self):
        # 入口url
        self.start_url = 'https://chs.meituan.com/meishi/'
        # 首先需要登录自己的账号上 获取登录后的Cookie信息和User-Agent来构造响应头
        self.headers = {
            # 修改成自己的cookie
            "Cookie": "_lxsdk_cuid=1716cdf4cd8c8-082ac455920bf48-49380f17-5a900-1716cdf4cd8c8; _hc.v=f17bef2e-9394-ea78-d6a7-940fc84143be.1614495157; mtcdn=K; ci=70; rvct=70%2C52; lsu=; uuid=99cbecdfcd6342ca9753.1617116140.1.0.0; _lx_utm=utm_source%3Dbaidu%26utm_medium%3Dorganic%26utm_term%3D%25E7%25BE%258E%25E5%259B%25A2; __mta=218988198.1617067475078.1617152337122.1617500202673.20; client-id=6cfcedec-72cb-470f-86a6-dddf64bc8869; lt=sOSqHk9WE66qIJX1xr-r9ytOpXsAAAAAJg0AAG99qBYNh2fwnJJ-MPffiG58lnM3m45u2teQdyug6LscHSf9jh_RDfoFcgz4UhgqfA; u=2585285025; n=%E9%A9%AC%E5%B0%91%E7%88%B1%E4%BD%A0%E4%B9%88%E4%B9%88%E5%93%92; token2=sOSqHk9WE66qIJX1xr-r9ytOpXsAAAAAJg0AAG99qBYNh2fwnJJ-MPffiG58lnM3m45u2teQdyug6LscHSf9jh_RDfoFcgz4UhgqfA; unc=%E9%A9%AC%E5%B0%91%E7%88%B1%E4%BD%A0%E4%B9%88%E4%B9%88%E5%93%92; firstTime=1617500314442; _lxsdk=17567c82defc8-02c8aee262bc18-3e604000-144000-17567c82defc8; _lxsdk_s=1789a866045-cd1-379-f7b%7C%7C6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        }
        # 初始化MongoDB数据库并创建数据库连接
        self.client = MongoClient()
        self.collection = self.client['test']['mt_foods']

    # 获取需要爬取的url列表
    def get_url_list(self,url,total_nums):
        url_temp = url+'pn{}/'
        # 每一页显示显示15个美食  通过获取到每个分类下的总美食数来求出总页数
        pages = total_nums//15+1 if total_nums%15!=0 else total_nums//15
        url_list = [url_temp.format(i) for i in range(1,pages+1)]
        return url_list

    # 对url进行请求并返回处理后的响应信息
    def parse_url(self,url):
        # self.headers['Cookie'] = random.choice(self.cookies)
        time.sleep(1)
        rest = requests.get(url,headers=self.headers)
        html_str = re.findall(r'window._appState = (.*?);</script>', rest.content.decode())[0]
        return html_str

    # 创建item并进行存储
    def get_content_list(self,html_str,item):
        json_html = json.loads(html_str)
        foods = json_html['poiLists']['poiInfos']
        for i in foods:
            item['food_id'] = i['poiId']
            item['food_url'] = "https://www.meituan.com/meishi/{}/".format(item['food_id'])
            item['title'] = i['title']
            item['avg_score'] = i['avgScore']
            item['avg_price'] = i['avgPrice']
            item['comments'] = i['allCommentNum']
            item['area'] = i['address'][0:3]
            item['address'] = i['address']
            print(item)
            self.save(item)
            
	# 保存数据到mongodb数据库中
    def save(self,item):
        self.collection.insert(item.copy())

    # 主方法
    def run(self):
        # 首先请求入口url来获取每一个美食分类的url地址
        # 请看图例一
        html_str = requests.get(self.start_url,headers=self.headers)
        print(html_str.content.decode())
        # 代码已经改变
        # html_str = html.etree.HTML(html_str.content.decode())
        # cate_list = html_str.xpath('//div[text()="分类"]/../ul/li')[1:]
        str_html = re.findall(r'window._appState = (.*?);</script>',html_str.content.decode())[0]
        json_html = json.loads(str_html)
        cate_list = json_html['filters']['cates'][1:]
        item_list = []

        # 对每一个分类进行分组分别获取美食的分类名和美食的分类的url
        for i in cate_list:
            item = {}
            # 分类的url进行反爬处理
            # 从网页中获取的url地址为 http://wx.meituan.com/meishi/c11/
            # 实际url地址为 https://wx.meituan.com/meishi/c11/
            # 因此需要将http替换成https
            # cate_url= i.xpath('./a/@href')[0]
            cate_url = i['url']
            item['cate_url'] = cate_url.replace('http','https')
            # item['cate_name'] = i.xpath('./a/text()')[0]
            item['cate_name'] = i['name']
            item_list.append(item)
        # 对每一个美食分类的分类名和分类url地址进行遍历并分别进行处理
        for i in item_list:
            # 睡眠1秒防止被识别为网络爬虫
            time.sleep(1)
            rest = requests.get(i['cate_url'],headers = self.headers)
            str_html = rest.content.decode()
            str_html = re.findall(r'window._appState = (.*?);</script>', str_html)[0]
            json_html = json.loads(str_html)
            total_nums = json_html['poiLists']['totalCounts']
            url_list = self.get_url_list(i['cate_url'],total_nums)
            for url in url_list:
                list_html = self.parse_url(url)
                self.get_content_list(list_html,i)


if __name__ == '__main__':
    meituan = MeituanSpider()
    meituan.run()

