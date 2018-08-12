# coding=utf-8
import os
import scrapy
from io import open
import json
import re
import requests
from scrapy.selector import Selector


class SpiderTang(scrapy.Spider):
    name = "poem"
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'

    def start_requests(self):
        urls = [
            'https://www.gushiwen.org/gushi/tangshi.aspx',
            # 'https://www.toutiao.com/ch/news_hot/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log('\n====>>>> get information from page: %s\n' % response.url)

        type = response.css("div.sons > div.typecont")

        for t in type:
            type_title = t.css("div.bookMl > strong::text").extract_first()
            self.log('\n====>>>> get poem type: %s\n' % type_title)
            poems = t.css("span > a")
            for p in poems:
                link = p.css("a::attr(href)").extract_first()
                yield scrapy.Request(url=link, callback=self.parse_poem, meta={'type': type_title})

        # type_title = type[0].css("div.bookMl > strong::text").extract_first()
        # poems = type[0].css("span > a")
        # link = poems[0].css("a::attr(href)").extract_first()
        # yield scrapy.Request(url=link, callback=self.parse_poem)

    def parse_poem(self, response):
        self.log('\n++++====>>>> get information from page: %s\n' % response.url)

        self.log('\n++++====>>>> sons counts: %s\n' % str(len(response.css("div.sons"))))

        # sons = response.css("div.main3 > div.left > div.sons")
        poem = response.css("div.sons")[0]
        title = poem.css("div.cont > h1::text").extract_first()
        author = poem.css("div.cont > p > a")[1].css("a::text").extract_first()

        content = ' '.join(poem.css("div.cont > div.contson::text").extract()).strip()
        if len(content) < 1:
            content = ' '.join(poem.css("div.cont > div.contson > p::text").extract()).strip()

        like_count = poem.css("div.tool > div.good > a > span::text").extract_first()
        tags = []
        for term in poem.css("div.tag > a"):
            tags.append(term.css("a::text").extract_first())
        tags_str = ' '.join(tags)

        translation_rsp = self.parse_translation(response)
        shangxi_rsp = self.parse_shangxi(response)
        background_rsp = self.parse_background(response)
        shangxi = shangxi_rsp['shangxi']
        translation = translation_rsp['translation']
        background = background_rsp['background']
        reference = shangxi_rsp['reference'] + ' ' + translation_rsp['reference'] + ' ' + background_rsp['reference']

        item = {
                'spider_name': self.name,
                'url': response.url,
                'type': response.meta['type'],
                'title': title,
                'author_name': author,
                'author_info': '',
                'content': content,
                'like_count': like_count,
                'tags': tags_str,
                'translation': translation,
                'shangxi': shangxi,
                'reference': reference,
                'background': background
        }

        return self.valid_item(item)

    def parse_background(self, response):
        background = ''
        reference = ''

        for block in response.css('div.sons'):
            column = block.css('div.sons > div.contyishang > div > h2 > span::text').extract_first()

            if column and u'背景' in column:
                background = ' '.join(block.css('div.contyishang > p::text').extract()).strip()
                reference = ' '.join(block.css('div.cankao > div > span::text').extract()).strip()
                break

        return {'background': background, 'reference': reference}

    def parse_shangxi(self, response):
        shangxi_blocks = response.xpath(u"//div[contains(@id, 'shangxi')]//a[contains(@href, 'shangxiShow')]").extract()

        shangxi = ''
        reference = ''

        if len(shangxi_blocks) > 0:
            for shangxi_block in shangxi_blocks:
                shangxi_code = re.findall(re.compile(r'[(](.*?)[)]', re.S), shangxi_block)[0]
                url = 'https://so.gushiwen.org/shiwen2017/ajaxshangxi.aspx'
                params = {'id': shangxi_code}
                rsp = requests.get(url, params=params)
                print(rsp.url)

                selector = Selector(text=rsp.text)
                shangxi += ' ' .join(selector.css('div.contyishang p::text').extract())
                reference += ' ' .join(selector.css('div.cankao span::text').extract())
        else:
            for block in response.css('div.sons'):
                column = block.css('div.sons > div.contyishang > div > h2 > span::text').extract_first()

                if column and (u'赏析' in column or u'鉴赏' in column):
                    shangxi += ' '.join(block.css('div.contyishang > p::text').extract()).strip()
                    reference += ' '.join(block.css('div.cankao > div > span::text').extract()).strip()

        return {'shangxi': shangxi, 'reference': reference}

    def parse_translation(self, response):

        fanyi_blocks = response.xpath(u"//div[contains(@id, 'fanyi')]//a[contains(@href, 'fanyiShow')]").extract()

        translation = ''
        reference = ''

        if len(fanyi_blocks) > 0:
            for fanyi_block in fanyi_blocks:
                fanyi_code = re.findall(re.compile(r'[(](.*?)[)]', re.S), fanyi_block)[0]
                url = 'https://so.gushiwen.org/shiwen2017/ajaxfanyi.aspx'
                params = {'id': fanyi_code}
                rsp = requests.get(url, params=params)
                print(rsp.url)

                selector = Selector(text=rsp.text)
                translation += ' '.join(selector.css('div.contyishang p::text').extract())
                reference += ' '.join(selector.css('div.cankao span::text').extract())
        else:
            for block in response.css('div.sons'):
                column = block.css('div.sons > div.contyishang > div > h2 > span::text').extract_first()

                if column and (u'译文' in column or u'注释' in column):
                    translation += ' '.join(block.css('div.contyishang > p::text').extract()).strip()
                    reference += ' '.join(block.css('div.cankao > div > span::text').extract()).strip()

        return {'translation': translation, 'reference': reference}

    def valid_item(self, item):
        for key in item.keys():
            if item[key] is not None:
                item[key] = item[key].strip()
                self.log("++++====>>>> " + item[key])
            else:
                item[key] = 'None'
                self.log("++++====>>>> " + item[key])
        return item
