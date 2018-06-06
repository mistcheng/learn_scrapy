import os
import scrapy
from io import open

class NewsSpider(scrapy.Spider):
    name = "news"

    write_path = '/Users/wind/WORK/code/learn_scrapy/data'

    def start_requests(self):
        urls = [
            'http://www.ifeng.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log('====>>>> get information from page: %s' % response.url)
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

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
        # pic = response.css('div.yc_con_txt > p.detalPic > img::attr(src)').extract_first()

        if title is None:
            title = response.css('div#artical > h1::text').extract_first()
            contents = response.css('div#main_content.js_selection_area > p')
            time = response.css('div#artical_sth > p.p_time > span[itemprop="datePublished"]::text').extract_first()
            source = response.css('div#artical_sth > p.p_time > span[itemprop="publisher"] > span[itemprop="name"]> a::text').extract_first()
            # pic = response.css('div#main_content.js_selection_area > p.detalPic > img::attr(src)').extract_first()

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

        if title is not None:
            # self.log('++++====>>>> %s' % title)
            # self.log('++++====>>>> %s' % contents_txt)
            self.log('++++====>>>> %s' % time.strip())
            self.log('++++====>>>> %s' % source.strip())
            self.log('++++====>>>> %s' % pic)

            # self.write_file(self.write_path, 'ifeng_top_news', contents_txt)

    def write_file(self, write_path, file_name, content):
        file_path = os.path.join(write_path, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            self.log('Saved file %s' % file_path)