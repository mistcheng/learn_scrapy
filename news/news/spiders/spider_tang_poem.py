# # coding=utf-8
# import os
# import scrapy
# from io import open
# import json
# import re
# import requests
#
#
# class SpiderTang(scrapy.Spider):
#     name = "poem"
#     USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
#
#     def start_requests(self):
#         urls = [
#             'https://www.gushiwen.org/gushi/tangshi.aspx',
#             # 'https://www.toutiao.com/ch/news_hot/'
#         ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)
#
#     def parse(self, response):
#         self.log('\n====>>>> get information from page: %s\n' % response.url)
#
#         type = response.css("div.sons > div.typecont")
#
#         for t in type[0:1]:
#             type_title = t.css("div.bookMl > strong::text").extract_first()
#             self.log('\n====>>>> get poem type: %s\n' % type_title)
#             poems = t.css("span > a")
#             for p in poems:
#                 link = p.css("a::attr(href)").extract_first()
#                 yield scrapy.Request(url=link, callback=self.parse_poem)
#
#         # type_title = type[0].css("div.bookMl > strong::text").extract_first()
#         # poems = type[0].css("span > a")
#         # link = poems[0].css("a::attr(href)").extract_first()
#         # yield scrapy.Request(url=link, callback=self.parse_poem)
#
#     def parse_poem(self, response):
#         self.log('\n++++====>>>> get information from page: %s\n' % response.url)
#
#         self.log('\n++++====>>>> sons counts: %s\n' % str(len(response.css("div.sons"))))
#
#         shangxi_ajax = response.xpath(u"//div[contains(@id, 'shangxi')]//a[contains(@href, 'shangxiShow')]").extract_first()
#         if len(shangxi_ajax) > 0:
#             shangxi_code = re.findall(re.compile(r'[(](.*?)[)]', re.S), shangxi_ajax)[0]
#             yield scrapy.Request(url='https://so.gushiwen.org/shiwen2017/ajaxshangxi.aspx?id=' + shangxi_code, callback=self.parse_shangxi)
#
#
#         sons = response.css("div.main3 > div.left > div.sons")
#         self.log(sons[0].body_as_unicode())
#         poem = response.css("div.sons")[0]
#         title = poem.css("div.cont > h1::text").extract_first()
#         dynasty = poem.css("div.cont > p > a")[0].css("a::text").extract_first()
#         author = poem.css("div.cont > p > a")[1].css("a::text").extract_first()
#         author_url = poem.css("div.cont > p > a::attr(href)").extract_first()
#
#         content = ' '.join(poem.css("div.cont > div.contson::text").extract())
#
#         like_count = poem.css("div.tool > div.good > a > span::text").extract_first()
#         tags = []
#         for term in poem.css("div.tag > a"):
#             tags.append(term.css("a::text").extract_first())
#         tags_str = ' '.join(tags)
#
#         translation_0 = ' '.join(response.css("div.sons")[1].css("div.contyishang > p").extract())
#         translation_1 = ' '.join(response.css("div.sons")[2].css("div.contyishang > p").extract())
#         if len(translation_0) >= len(translation_1):
#             translation = translation_0
#         else:
#             translation = translation_1
#
#         translation_like_0 = ' '.join(response.css("div.sons")[1].css("div.dingpai > a::text").extract())
#         translation_like_1 = ' '.join(response.css("div.sons")[2].css("div.dingpai > a::text").extract())
#
#         if len(translation_like_0) >= len(translation_like_1):
#             translation_like = translation_like_0
#         else:
#             translation_like = translation_like_1
#
#         shangxi = ' '.join(response.css("div.sons")[3])
#
#         item = {
#                 'spider_name': self.name,
#                 'poem_url': response.url,
#                 'title': title,
#                 'dynasty': dynasty,
#                 'author': author,
#                 'author_url': author_url,
#                 'content': content,
#                 'like_count': like_count,
#                 'tags': tags_str,
#                 'translation': translation,
#                 'translation_like': translation_like
#         }
#
#         return self.valid_item(item)
#
#
#     def parse_shangxi(self, response):
#         return ''
#
#
#     def valid_item(self, item):
#         for key in item.keys():
#             if item[key] is not None:
#                 item[key] = item[key].strip()
#                 self.log("++++====>>>> " + item[key])
#             else:
#                 item[key] = 'None'
#                 self.log("++++====>>>> " + item[key])
#         return item
