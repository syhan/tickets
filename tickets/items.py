# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose

class PiaoniuEvent(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    desc = scrapy.Field()
    time = scrapy.Field()
    venue = scrapy.Field()
    id = scrapy.Field()
    meta = scrapy.Field()
    ticket_categories = scrapy.Field()
    tickets = scrapy.Field()

class PiaoniuEventLoader(ItemLoader):
    default_output_processor = TakeFirst()
    id_in = MapCompose(lambda x: re.sub(r'\D', '', x))