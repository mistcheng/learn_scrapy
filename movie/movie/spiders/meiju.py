# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class MeijuSpider(scrapy.Spider):
    name = 'meiju'
    allowed_domains = ['23wx.com']
    start_urls = ['http://www.23wx.com/class/']

    def start_requests(self):
        for i in range(1, 11):
            url = self.start_urls + str(i) + '_1.html'
            yield Request(url, self.parse())
        yield Request('http://www.23wx.com/quanben/1', self.parse())

    def parse(self, response):
        print(response.text)
