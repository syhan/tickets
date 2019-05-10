# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from tickets.items import PiaoniuEvent, PiaoniuEventLoader

class PiaoniuSpider(scrapy.Spider):
    name = 'piaoniu'
    allowed_domains = ['www.piaoniu.com']
    start_urls = ['http://www.piaoniu.com/sh-all']

    def parse(self, response):
        for a in response.css('li.item'):
            l = PiaoniuEventLoader(item=PiaoniuEvent(), selector=a)

            l.add_css('title', 'div.info div.title a::text')
            l.add_css('desc',  'div.info div.desc::text')
            l.add_css('time',  'div.info div.time::text')
            l.add_css('venue', 'div.info a.venue::text')
            l.add_css('id',    'div.seo-buy a::attr(href)')

            yield l.load_item()

        next_page = response.xpath('//li[a="下一页"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        
