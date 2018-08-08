# coding=utf-8

import sys
import MySQLdb
# import redis
import os
import time


def import_to_redis():
    db = MySQLdb.connect(host='172.16.176.126', db='CPD_REC_V1', user='mysqluser', passwd='mysqluser')
    # ad_redis = redis.StrictRedis('172.16.178.60', 6372)
    cursor = db.cursor()
    cursor.execute('select * from mdl_fdt_apps_ad_new_info_d limit 2')
    i = 0
    a = []
    for i in range(0, 22):
        a.append('a' + str(i))
        print a[i]
    results = cursor.fetchall()
    for result in results:
        aid = result[0]
        for j in range(0, 22):
            if result[j] != None:
                # ad_redis.hset(aid,a[j],result[j])
                # print("%s %s %s" % (aid,a[j],result[j]))
                print result[j]


if __name__ == "__main__":
    import_to_redis()
    print "import redis"
