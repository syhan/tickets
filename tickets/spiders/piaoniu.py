# -*- coding: utf-8 -*-
import scrapy


class PiaoniuSpider(scrapy.Spider):
    name = 'piaoniu'
    allowed_domains = ['www.piaoniu.com']
    start_urls = ['http://www.piaoniu.com/sh-concerts']

    def parse(self, response):
        for activity in response.css('li.item'):
            yield {
                'title': activity.css('div.info div.title a::text').get()
            }

        next_page = response.xpath('//li[a="下一页"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        
