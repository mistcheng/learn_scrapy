import scrapy


class WeatherSpider(scrapy.Spider):
    name = "weather"

    def start_requests(self):
        urls = [
            'http://www.weather.com.cn/weather1d/101280601.shtml',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log("====>>>> get information from page: %s" % response.url)
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

        page_title = response.css('title::text').extract_first()
        self.log("====>>>> page title: %s" % page_title)

        temp = response.css('div.tem > span::text').extract_first()
        self.log("====>>>> temp: %s" % temp)

