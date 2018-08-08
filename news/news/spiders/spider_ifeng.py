import os
import scrapy
from io import open


class SpiderIfeng(scrapy.Spider):
    name = "news_ifeng"

    def start_requests(self):
        urls = [
            'http://www.ifeng.com/',
            # 'https://www.toutiao.com/ch/news_hot/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log('====>>>> get information from page: %s' % response.url)

        news_list = response.css("div#headLineDefault > ul.FNewMTopLis > ul > li")

        for item in news_list:
            news_link = item.css('a')
            for li in news_link:
                title = li.css('a::text').extract_first()
                link = li.css('a::attr(href)').extract_first()
                self.log('====>>>> title: %s' % title)
                self.log('====>>>> link: %s' % link)
                yield scrapy.Request(url=link, callback=self.parse_1)

    def parse_1(self, response):
        self.log('++++====>>>> get information from page: %s' % response.url)

        title = response.css('div.yc_tit > h1::text').extract_first()
        contents = response.css('div.yc_con_txt > p')
        time = response.css('div.yc_tit > p > span::text').extract_first()
        source = response.css('div.yc_tit > p > a::text').extract_first()

        if title is None:
            title = response.css('div#artical > h1::text').extract_first()
            contents = response.css('div#main_content.js_selection_area > p')
            time = response.css('div#artical_sth > p.p_time > span[itemprop="datePublished"]::text').extract_first()
            source = response.css('div#artical_sth > p.p_time > span[itemprop="publisher"] > span[itemprop="name"]> a::text').extract_first()

        pic = None
        for p in contents:
            temp = p.css('p.detailPic > img::attr(src)').extract_first()
            if temp is not None:
                pic = temp

        contents_txt = ''
        temp = []
        for cont in contents:
            paragraph = cont.css('p::text').extract_first()
            if paragraph is not None:
                temp.append(paragraph)
        if len(temp) > 0:
            contents_txt = '\n'.join(c for c in temp)

        item = {
                'spider_name': self.name,
                'news_url': response.url,
                'title': title,
                'source': source,
                'time': time,
                'content': contents_txt,
                'image_url': pic,
                'video_url': pic
        }

        return self.valid_item(item)

    def valid_item(self, item):
        for key in item.keys():
            if item[key] is not None:
                item[key] = item[key].strip()
                self.log("++++====>>>> " + item[key])
            else:
                item[key] = 'None'
                self.log("++++====>>>> " + item[key])
        return item
