# coding:utf8
import random

import requests
import time
import re
import redis
import os
from multiprocessing import Process,Queue


class QiuShiSpider():
    def __init__(self):
        self.a=1
        self.user_agent = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        self.headers = {
            'User-Agent': random.choice(self.user_agent)
        }
        self.ip_list = [

        ]
        self.proxy = ''
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.r = redis.Redis(connection_pool=pool)

    def get_page(self, page):
        URL = 'https://www.qiushibaike.com/8hr/page/%s/' % page
        html = requests.get(URL, headers=self.headers, proxies=self.proxy)
        # print(html.text)
        return html.text

    # def get_data2(self,page):
    #
    #     html=self.get_page(page)
    #     # print(html)
    #     print(1)
    #     pattern=re.compile(u'<a.*?>.*?<div.*?class="content">.*?<span>(.*?)</span>.*?</div>.*?</a>',re.S)
    #     content=re.findall(pattern,html)
    #     print(len(content))
    #     print(content)

    # def get_data(self, page):
    #     html = self.get_page(page)
    #     content=[]
    #     content_item3=[]
    #     content_pattern1=re.compile(r'<div.*?class="article block.*?".*?>.*?<a.*?>.*?<div.*?class="content">.*?<span>(.*?)</span>.*?</div>.*?</a>.*?</div>',re.S)
    #     content_pattern2 = re.compile(r'<div.*?class="content">.*?<span>(.*?)</span>.*?</div>.*?<div.*?class="thumb">.*?<img.*?src="(.*?)".*?>.*?</div>', re.S)
    #
    #     content_item1 = re.findall(content_pattern1, html)
    #     print(len(content_item1))
    #     content_item2 = re.findall(content_pattern2, html)
    #     print(len(content_item2))
    #     for v in content_item2:
    #         content_item3.append(v[0])
    #     for i in content_item1:
    #         if i not in content_item3:
    #             content.append(i)
    #     print(len(content))
        # self.storage_in_redis(content)

    def get_data(self,page,q):
        content_pattern = re.compile(
            r'<div.*?class="article block.*?".*?>.*?<a.*?>.*?<div.*?class="content">.*?<span>(.*?)</span>.*?</div>.*?</a>.*?</div>',
            re.S)
        for v in range(1,page):
            print("第%s页开始。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。"%page)
            content = []
            html=self.get_page(page)

            content_item=re.findall(content_pattern,html)
            for v in content_item:
                if len(v)>25:
                    content.append(v)
                    print(v)
            q.put(content)
            print('第%s页已加入队列'%page)
            print("第%s页结束。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。"%page)
            time.sleep(1)

    def storage_in_redis(self,q):
        while True:
            content=q.get(True)
            for v in content:
                self.r.zadd('qiushicontent',v,self.a)
                print("第%s条数据存储成功！"%self.a)
                self.a += 1
            print("###############################一页存储成功！##############################################")
            time.sleep(1)

    def hello(self,name):
        print('Run task %s (%s)...' % (name, os.getpid()))
        start = time.time()
        time.sleep(random.random() * 3)
        end = time.time()
        print('Task %s runs %0.2f seconds.' % (name, (end - start)))

    def main(self):
        print("开始从糗事爬取。。。")
        print("parent is %s" % os.getpid())
        q=Queue
        p=Process(target=self.get_data,args=(4,q,))
        sql=Process(target=self.storage_in_redis,args=(q,))
        p.start()
        sql.start()
        p.join()
        sql.terminate()
        print('done!')
        print('抓取完毕！')


if __name__ == '__main__':
    spider = QiuShiSpider()
    spider.main()
