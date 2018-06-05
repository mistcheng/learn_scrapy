import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        # define the urls for scrapy
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        # generate requests from urls (could be omitted)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        self.log(filename)
        # # self.log(response.body)
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

        title = response.css('title::text').extract_first()
        self.log(title)
        for quote in response.css('div.quote'):
            quote_text = quote.css('span.text::text').extract_first()
            quote_author = quote.css('small.author::text').extract_first()
            self.log(quote_text)
            self.log(quote_author)