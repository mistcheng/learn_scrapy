import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"

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
        # content = response.css('div.yc_con')

        self.log('++++====>>>> %s' % title)