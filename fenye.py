import csv
import json
import random
import re
import sys
import threading
import time
import httplib2
from lxml import etree
import requests
from queue import Queue
import redis
from jd.Mylog import Logger
from urllib.parse import urljoin
import hashlib


class JD:
    def __init__(self, url_list):
        self.myredis = redis.Redis(host="localhost",port=6379)
        self.a = hashlib.md5()
        for i in url_list:
            self.a.update(bytes(i,encoding='utf-8'))
            result = self.a.hexdigest()
            if not self.myredis.sismember("jdset",result):
                self.myredis.sadd("jdset",result)
                self.myredis.lpush("jdu",i)
        self.url1 = "https://p.3.cn/prices/mgets?area=10_698_0_0&skuIds=J_{}"
        self.url2 = "https://item.jd.com/{}.html"
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 "
            "Safari/537.36",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;TencentTraveler4.0;.NETCLR2.0.50727)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        ]
        self.data_queue = Queue()
        self.logger = Logger(log_file_name='log.txt',  logger_name="test").get_log()
        self.baseurl = "https://list.jd.com"
        self.R=threading.Lock()

    def getRespon(self):
        while self.myredis.lrange("jdu",0,-1):
            url = str(self.myredis.lpop("jdu"), encoding='utf-8')
            # print(url)
            all_goods = []
            headers = {
                'User-Agent': random.choice(self.ua_list),
                 'Connection': 'close',
            }
            headers1 = {
                'User-Agent': random.choice(self.ua_list),
                'Referer': url,
                 'Connection': 'close',
            }

            # 对解析出的列表页，取出id、name
            get_res = httplib2.Http()
            try:
                response, context = get_res.request(url, method='GET', headers=headers)
            except Exception as e:
                self.logger.error(e)
                time.sleep(10)
                response, context = get_res.request(url, method='GET', headers=headers)
            if response["status"] != '200':
                sys.exit(0)
            context = str(context, encoding='utf-8')
            html = etree.HTML(context)
            shops = html.xpath('//ul[@class="gl-warp clearfix"]/li')
            next_url =html.xpath('//a[@class="pn-next"]/@href')[0]
            if next_url is not None:
                next_url = urljoin(self.baseurl,next_url)
                self.a.update(bytes(next_url,encoding='utf-8'))
                result = self.a.hexdigest()
                if not self.myredis.sismember("jdset", result):
                    self.myredis.sadd("jdset", result)
                    self.myredis.lpush("jdu",next_url)
            for i in shops:
                item = {}
                id = "".join(i.xpath("./div/@data-sku"))
                if id is None:
                    self.logger.warn("%s 不能用"%url)
                    break
                item["id"] = "".join(id.split())
                id_redis = item["id"]
                if not self.myredis.sismember('jd',id_redis):
                    self.myredis.sadd('jd',id_redis)
                    b = "".join(i.xpath("./div/div[3]/a/em/text()"))
                    if not b:
                        b = "".join(i.xpath("./div/div[4]/a/em/text()"))
                    item["name"] = "".join(b.split())
                    print(item["name"])
                    # 解析详情页，获得店铺名称，以及是否是自营
                    url2 = self.url2.format(item["id"])
                    #print(url2)
                    s =requests.session()
                    s.keep_alive =False
                    res1 = s.get(url2, headers=headers).text
                    result1 = re.compile(r'dianpuname1">(.*?)</a>', re.S)
                    try:
                        shop = result1.findall(res1)[0]
                    except:
                        shop =None
                        self.logger.debug("%s 无法访问店铺名称"%url2)
                        # print(url2+"无法访问店铺名称")
                    item["shop"] = shop
                    print(item['shop'])
                    result = re.compile(r'<em class="u-jd">(.*?)</em>', re.S)
                    try:
                        ziying = result.findall(res1)[0].split()[0]
                    except:
                        ziying = 'null'
                    if "自营" in ziying:
                        item["zy"] = True
                    else:
                        item["zy"] = False
                    url1 = self.url1.format(item.get("id"))
                    # 解析json，拿到价格、其中也可以找到对应的网址，拿到评论。
                    res = s.get(url1, headers=headers1).text
                    item["price"] = json.loads(res)[0]["op"]
                    all_goods.append(item)
                    time.sleep(1)
                else:
                    self.logger.debug("该商品已经存在%s"%id_redis)
            self.data_queue.put(all_goods)
            self.logger.debug("%s 抓取完成"%url)

    def store(self):
        while self.data_queue.not_empty:
            print("ok")
            goods = self.data_queue.get()
            self.data_queue.task_done()
            fff = open('jd.csv', 'a',newline='')
            title = ["id", "name", "price", "zy", "shop"]
            fil = csv.DictWriter(fff,fieldnames=title)
            for i in goods:
                fil.writerow(i)
            fff.close()

    def main(self):
        thread_list =[]
        for i in range(2):
            thread_url = threading.Thread(target=self.getRespon)
            thread_list.append(thread_url)
        for i in range(2):
            thread_save = threading.Thread(target=self.store)
            thread_list.append(thread_save)
        for th in thread_list:
            th.setDaemon(True)
            th.start()
        for i in thread_list:
            i.join()
        self.data_queue.join()
        time.sleep(3)


if __name__ == '__main__':
    url_list = []
    with open('url.txt', 'r') as f:
        data = f.readlines()
        for i in data:
            i = i.split()
            url_list.extend(i)
    a = JD(url_list)
    # a = JD("https://list.jd.com/list.html?cat=9987,653,655")
    a.main()
