# jdcrawler
一个简单的京东爬虫，包含了一些去重，ajax以及增量爬虫
## [geturl.py](https://github.com/shawmoden/jdcrawler/edit/master/geturl.py)
  通过selenium找到了jd所有的url连接
## [index.py](https://github.com/shawmoden/jdcrawler/edit/master/index.py)
  进行url的筛选，有些url一次无法使用
## main.py(https://github.com/shawmoden/jdcrawler/edit/master/main.py)
  通过Redis进行持久化，找到ajax网址，发送带Referer的headers获取价格、评价等数据。使用logging记录部分信息。
## 其他的文件说明
  url.txt表示可以使用的url地址
  url1.txt表示需要进行第二次提取
  jd.csv表示抓取的部分结果
  log.txt 输出的部分日志
  
