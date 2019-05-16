# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import json
import datetime
import os

from influxdb import InfluxDBClient

MEASUREMENT = 'ticket_price'

class PiaoNiuEventMetaPipeline(object):
    META_URL = 'https://www.piaoniu.com/api/v1/activities/{}.json'

    def process_item(self, item, spider):
        if spider.name == 'piaoniu':
            resp = requests.get(self.META_URL.format(item['id']))
            if resp.ok:
                item['meta'] = json.loads(resp.text)
        
        return item

class PiaoNiuTicketCategoriesPipeline(object):
    TICKET_CATEGORIES_URL = 'https://www.piaoniu.com/api/v1/ticketCategories.json?b2c=true&eventId={}'

    def process_item(self, item, spider):
        if spider.name == 'piaoniu':
            events = item['meta']['events']
            item['ticket_categories'] = [] # initialize ticket categories 

            for event in events:
                resp = requests.get(self.TICKET_CATEGORIES_URL.format(event['id']))

                if resp.ok:
                    item['ticket_categories'] += json.loads(resp.text) # concatenate if necessary
        
        return item

class PiaoNiuTicketPipeline(object):
    TICKET_URL = 'https://www.piaoniu.com/api/v4/tickets.json?b2c=true&eventId={}&ticketCategoryId={}'

    def process_item(self, item, spider):
        if spider.name == 'piaoniu':
            item['tickets'] = {}
            ticket_categories = item['ticket_categories']

            for c in ticket_categories:
                resp = requests.get(self.TICKET_URL.format(c['activityEventId'], c['id']))

                if resp.ok:
                    item['tickets'][c['id']] = json.loads(resp.text)
        
        return item

class PiaoNiuPointsPipeline(object):

    def process_item(self, item, spider):
        if spider.name == 'piaoniu':

            def category_to_point(c):
                point = {}
                point['measurement'] = MEASUREMENT
                point['tags'] = {
                    'name': item['title'], 
                    'desc': item.get('desc'), 
                    'venue': item['venue'], 
                    'date': item['time'], 
                    'source': item['source'],
                    'url': item['url'],
                    'origin_price': c['originPrice']
                }
                point['fields'] = {'price': c['lowPrice']}
                point['time'] = str(datetime.datetime.now())

                return point

            item['points'] = list(map(category_to_point, filter(lambda c: c.get('lowPrice'), item['ticket_categories'])))
            
        return item


class MoreTicketsSessionPipeline(object):
    SESSION_URL = 'https://www.moretickets.com/showapi/pub/v1_2/show/{}/sessionone'

    def process_item(self, item, spider):
        if spider.name == 'moretickets':
            resp = requests.get(self.SESSION_URL.format(item['id']))
            if resp.ok: 
                item['session'] = json.loads(resp.text)
            elif resp.status_code == 555: # occasionally it failed, consider retry

                # avoid recursive invoke since there's no counter in parameter
                resp = requests.get(self.SESSION_URL.format(item['id']))
                if resp.ok: 
                    item['session'] = json.loads(resp.text)

        return item

class MoreTicketsPointsPipeline(object):

    def process_item(self, item, spider):
        if spider.name == 'moretickets' and item.get('session'):

            def seatplan_to_point(s):
                point = {}
                point['measurement'] = MEASUREMENT
                point['tags'] = {
                    'name': item['name'],
                    'desc': item.get('desc'), 
                    'venue': item['venue'], 
                    'date': item['time'], 
                    'source': item['source'],
                    'url': item['url'],
                    'origin_price': s['originalPrice']
                }
                point['fields'] = {'price': s['minPrice']}
                point['time'] = str(datetime.datetime.now())

                return point

            d = item['session']['result']['data']
            if len(d) > 0:
                item['points'] = list(map(seatplan_to_point, filter(lambda p: p.get('minPrice'), d[0]['seatplans'])))

        return item


class SourcePipeline(object):

    def process_item(self, item, spider):
        item['source'] = spider.name

        return item
        

class InfluxDbPipeline(object):

    def __init__(self, influx_uri, influx_port, influx_db):
        self.influx_uri = influx_uri
        self.influx_port = influx_port
        self.influx_db = influx_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            influx_uri = os.getenv('INFLUX_URL', crawler.settings.get('INFLUX_URL')),
            influx_port = os.getenv('INFLUX_PORT', crawler.settings.get('INFLUX_PORT')),
            influx_db = os.getenv('INFLUX_DATABASE', crawler.settings.get('INFLUX_DATABASE'))
        )

    def open_spider(self, spider):
        self.client = InfluxDBClient(host=self.influx_uri, port=self.influx_port)
        self.client.create_database(self.influx_db)
        self.client.switch_database(self.influx_db)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item.get('points'):
            self.client.write_points(item['points'])

        return item