#coding:utf8

import redis

pool = redis.ConnectionPool(host='localhost',port=6379,db=0)
r=redis.Redis(connection_pool=pool)
china=r.get('china')
value=r.zrange('qiushicontent',0,53)
str='这小编的数学是体育老师教的吧'
print(len(str))