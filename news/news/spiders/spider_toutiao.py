# coding=utf-8
import scrapy
import json
import re
from utils import parse_js_1
import yaml

class SpiderTouTiao(scrapy.Spider):
    name = "news_toutiao"

    def start_requests(self):
        urls = [
            # 'https://www.toutiao.com/ch/news_hot/'
            'https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1E51BE2660392B&cp=5B26B379327B3E1&_signature=y44DiAAAkLB0-PJu.D5-QMuOA5'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log('====>>>> get information from page: %s' % response.url)

        news_info = json.loads(response.body_as_unicode())

        base_url = "https://www.toutiao.com"
        for info in news_info["data"]:
            url_temp = base_url + info["source_url"]
            yield scrapy.Request(url=url_temp, callback=self.parse_1)

    def parse_1(self, response):
        self.log('++++====>>>> get information from page: %s' % response.url)

        temp = re.findall(pattern='var BASE_DATA = ({.+});</script>', string=response.body.decode('utf-8'), flags=re.M | re.U | re.S)

        # temp = re.findall(pattern='articleInfo: ({.+})', string=response.body.decode('utf-8'), flags=re.M | re.U | re.S)

        if len(temp) > 0:
            temp_str = temp[0].replace(".replace(/<br \/>/ig, '')", '')
            # self.log(temp_str)

            temp_dict = yaml.load(temp_str)
            title = temp_dict['articleInfo']['title']
            content = temp_dict['articleInfo']['content']
            source = temp_dict['articleInfo']['subInfo']['source']
            time = temp_dict['articleInfo']['subInfo']['time']
            image_url = ''
            video_url = ''
            comment_count = temp_dict['shareInfo']['commentCount']
            tag_dict = temp_dict['articleInfo']['tagInfo']['tags']
            tags = []
            if len(tag_dict) > 0:
                for t in tag_dict:
                    tags.append(t['name'])
            tags_str = '|'.join(tags)

            item = {
                'spider_name': self.name,
                'news_url': response.url,
                'title': title,
                'source': source,
                'time': time,
                'content': content,
                'image_url': image_url,
                'video_url': video_url,
                'comment_count': comment_count,
                'tags': tags_str
            }
            return self.valid_item(item)
        else:
            self.log("++++====>>>> lalal")


    def valid_item(self, item):
        for key in item.keys():
            if item[key] is not None:
                item[key] = item[key].strip()
                self.log("++++====>>>> " + item[key])
            else:
                item[key] = 'None'
                self.log("++++====>>>> " + item[key])
        return item
