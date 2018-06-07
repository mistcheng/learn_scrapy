# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import pymysql
import settings
from scrapy import log


class NewsPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(host=settings.MYSQL_HOST,
                                       db=settings.MYSQL_DBNAME,
                                       user=settings.MYSQL_USER,
                                       passwd=settings.MYSQL_PASSWD,
                                       charset='utf8',
                                       use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test = "123"
        sql = "insert into news.ifeng(title, news_url, source, time, content, image_url, video_url, time_in) " \
              "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                item['title'],
                item['news_url'],
                item['source'],
                item['time'],
                item['content'],
                item['image_url'],
                item['video_url'],
                now)

        # sql = "insert into news.ifeng(title, source, time, content, image, video, time_in) " \
        #       "values('%s', '%s', '%s', '%s', '%s', '%s', '%s')"

        print(sql)

        try:
            # self.my_db_cursor.execute(sql, (item['title'].encode('utf-8'),
            #                                 item['source'].encode('utf-8'),
            #                                 item['time'].encode('utf-8'),
            #                                 item['content'].encode('utf-8'),
            #                                 item['image'].encode('utf-8'),
            #                                 item['video'].encode('utf-8'),
            #                                 now.encode('utf-8')))
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            print("++++====>>>> Error %d: %s" % (e.args[0], e.args[1]))

        # finally:
        #     self.connect.close()

        return item
