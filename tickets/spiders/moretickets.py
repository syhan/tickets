# -*- coding: utf-8 -*-
import scrapy

from tickets.items import MoreTicketsEvent, MoreTicketsEventLoader

class MoreTicketsSpider(scrapy.Spider):
    name = 'moretickets'
    allowed_domains = ['www.moretickets.com']
    start_urls = ['https://www.moretickets.com/list/3101-all/hottest']

    def parse(self, response):
        for a in response.css('div.shows-container a.show-items.sa_entrance'):
            l = MoreTicketsEventLoader(item=MoreTicketsEvent(), selector=a)

            l.add_css('name', 'div.show-name::text')
            l.add_css('desc',  'div.show-desc::text')
            l.add_css('time',  'div.show-time::text')
            l.add_css('venue', 'div.show-addr::text')
            l.add_css('id',    'a::attr(href)')
            l.add_css('url',    'a::attr(href)')

            yield l.load_item()

        next_page = response.css('div.icon.icon-page-next').get()
        if next_page is not None:
            url = response.css('li.pagination-page:last-child a::attr(href)').get()
            yield response.follow(url, callback=self.parse)