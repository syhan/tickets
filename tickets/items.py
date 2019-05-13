# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose

class PiaoNiuEvent(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    time = scrapy.Field()
    venue = scrapy.Field()
    id = scrapy.Field()
    meta = scrapy.Field()
    ticket_categories = scrapy.Field()
    tickets = scrapy.Field()
    points = scrapy.Field()
    source = scrapy.Field()

class PiaoNiuEventLoader(ItemLoader):
    default_output_processor = TakeFirst()
    id_in = MapCompose(lambda x: re.sub(r'\D', '', x))


class MoreTicketsEvent(scrapy.Item):
    name = scrapy.Field()
    desc = scrapy.Field()
    time = scrapy.Field()
    venue = scrapy.Field()
    id = scrapy.Field()
    session = scrapy.Field()
    points = scrapy.Field()
    source = scrapy.Field()

class MoreTicketsEventLoader(ItemLoader):
    default_output_processor = TakeFirst()
    id_in = MapCompose(lambda x: re.sub(r'/content/', '', x))

