# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import pymysql
import settings
from codecs import open
import json


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

        if item['spider_name'] == 'news_ifeng':
            sql = """
                insert into news.ifeng(title, news_url, source, time, content, image_url, video_url, time_in) 
                values(%s, %s, %s, %s, %s, %s, %s, %s) 
                ON DUPLICATE KEY UPDATE title=%s, source=%s, time=%s, content=%s
            """

            args = (item['title'], item['news_url'], item['source'], item['time'], item['content'], item['image_url'],
                   item['video_url'], now, item['title'], item['source'], item['time'], item['content'])

            # print(sql)

            try:
                self.cursor.execute(sql, args)
                self.connect.commit()
            except Exception as e:
                print("++++====>>>> Error %d: %s" % (e.args[0], e.args[1]))

            # finally:
            #     self.connect.close()
        elif item['spider_name'] == 'news_toutiao':
            sql = """
            insert into news.toutiao(title, news_url, source, time, content, image_url, video_url, time_in, 
                  comment_count, tags) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                  ON DUPLICATE KEY UPDATE title=%s, source=%s, time=%s, content=%s
            """

            args = (item['title'], item['news_url'], item['source'], item['time'], item['content'], item['image_url'],
                    item['video_url'], now, item['comment_count'], item['tags'], item['title'], item['source'],
                    item['time'], item['content'])
            # print(sql)

            try:
                self.cursor.execute(sql, args)
                self.connect.commit()
            except Exception as e:
                print("++++====>>>> Error %d: %s" % (e.args[0], e.args[1]))

            # finally:
            #     self.connect.close()
        elif item['spider_name'] == 'poem':
            print("\n++++>>>> hahh \n")
            # with open('/Users/wind/WORK/code/learn_scrapy/data/poem.txt', 'a+', 'utf-8') as ouf:
            #     # for k, v in item.items():
            #     #     ouf.write(k + ">>><<<" + v + "\n")
            #     ouf.write(json.dumps(item))
            #
            # sql = "insert into news.poem(poem_url, title, dynasty, author, author_url, content, like_count, tags, translation, translation_like, time_in) " \
            #       "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
            #           item['poem_url'],
            #           item['title'],
            #           item['dynasty'],
            #           item['author'],
            #           item['author_url'],
            #           item['content'],
            #           item['like_count'],
            #           item['tags'],
            #           item['translation'],
            #           item['translation_like'],
            #           now)
            # print(sql)
            #
            # try:
            #     self.cursor.execute(sql)
            #     self.connect.commit()
            # except Exception as e:
            #     print("++++====>>>> Error %d: %s" % (e.args[0], e.args[1]))

        else:
            print('++++====>>>> hahaah')
        return item
