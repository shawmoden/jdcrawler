import random
import re
import sys
import threading

import redis
import pandas as pd
import pymysql
from urllib.parse import urljoin
import requests
import httplib2
# url = "https://list.jd.com/list.html?cat=737,794,798&ev=4155_76344&sort=sort_rank_asc&trans=1&JL=2_1_0#J_crumbsBar"
# url1 = "https://p.3.cn/prices/mgets?area=10_698_0_0&skuIds=J_7185303"
# #
# list =["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
#        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
#        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 "
#        "Safari/537.36",
#        "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;TencentTraveler4.0;.NETCLR2.0.50727)",
#        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" ,
#        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
#        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
#        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
#        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
#        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
#        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
#        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
#        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
#        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
#        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
#        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
#        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
#        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
#        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
#        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
#        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
#        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
# ]
# for i in range(15):
from lxml import etree

headers = {
'User-Agent':"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
}
#     print(headers)
# res =[{"cbf":"0","id":"J_100002749549","m":"10000.00","op":"4288.00","p":"4278.00"}][0]
# res =requests.get(url1,headers=headers).text
# print(res)

# # print(res["op"])
# list =['100002749549'
#        '123']
# # a ="".join(list)
# # print(a)
# # a =a.split()
# # # print(a)
# baseurl ="https://list.jd.com"
# res =requests.get("https://list.jd.com/list.html?cat=737,794,798&ev=4155_97865&sort=sort_rank_asc&trans=1&JL=3_%E7%94%B5%E8%A7%86%E7%B1%BB%E5%9E%8B_%E5%85%A8%E9%9D%A2%E5%B1%8F#J_crumbsBar",headers =headers).text
# html =etree.HTML(res)
# url =html.xpath('//a[@class="pn-next"]/@href')[0]
#
# if url!=None:
#     next_url =urljoin(baseurl,url)
#     print(next_url)

# list =[{'id':123,'name':'abc'},{'id':1234,'name':'abcd'}]
# data =pd.DataFrame(list).to_csv("test.csv")
# url = "https://www.baidu.com"
# url1 = "//baidu.com/cn"
# # url3 =urljoin(url,url1)
# # print(url3)
# list =[]
# with open("url.txt","r") as f:
#     data =f.readlines()
#     for i in data:
#         i =i.split()
#         list.extend(i)
#     print(len(list))
import logging
# import csv
# from jd.Mylog import Logger
# #
#
# item1 =[{"id":456,"name":"apple"},{"id":123,"name":"huawei"}]
# f =open('test.csv','a',newline="")
# liss =["id","name"]
# fi =csv.DictWriter(f,fieldnames=liss)
# for i in item1:
#     fi.writerow(i)
# f.close()
# #
# ht =httplib2.Http()
# res ,con =ht.request("https://www.baidu.com",method="GET",headers=headers)
#
# if '200' == res['status']:
#     print("oooo")
#     sys.exit()
#
# # # print("ok")
# res =requests.get("https://i-item.jd.com/7929946.html",headers=headers).text
# result = re.compile(r'<em class="u-jd">(.*?)</em>', re.S)
# ziying = result.findall(res)[0].split()[0]
# if "自营" in ziying:
#     print("True")
# con =redis.StrictRedis()
# # # # if not con.sismember("jd","123"):
# # # #     print("ok")
# # #
# # # # print(con.lrange("jdu",0,-1))
# conut =0
# while con.lrange("jdu",0,-1):
#     conut+=1
#     print(conut)
# # print([] == None)
# class ASD:
#     def test(self):
#         while True:
#             print("123")
#     def tes(self):
#         for i in range(3):
#             print("ok")
#     def main(self):
#         a =threading.Thread(target=self.test)
#         b =threading.Thread(target=self.tes)
#         a.setDaemon(True)
#         b.setDaemon(True)
#         a.start()
#         b.start()
#
# if __name__ == '__main__':
#     a =ASD()
# #     a.main()
# list =[]
# if not list:
#     print("ok")
s =requests.session()
s.keep_alive=False
respon =s.get("https://www.baidu.com")
print(respon.text)