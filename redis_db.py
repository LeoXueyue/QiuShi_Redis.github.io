#coding:utf8

import redis

# r=redis.StrictRedis(host='localhost',port=6379,db=0)
# me1=r.get('me')
# print(me1)
pool = redis.ConnectionPool(host='localhost',port=6379,db=0)
r=redis.Redis(connection_pool=pool)
# for i in range(20):
#     url='http://www.qiushibaike.com/hot/page/%d/'%(i+1)
#     r.sadd('urls',url)
#
# urls=r.smembers('urls')

for i in range(20):
    url = 'http://www.qiushibaike.com/hot/page/%d/' % (i + 1)
    r.zadd('luyou',url,i)
    print('%s done！'%i)

luyou = r.zrange('luyou',0,20)
print(luyou)