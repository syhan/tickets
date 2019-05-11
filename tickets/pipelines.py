# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import json

class EventMetaPipeline(object):
    META_URL = 'https://www.piaoniu.com/api/v1/activities/{}.json'

    def process_item(self, item, spider):
        resp = requests.get(self.META_URL.format(item['id']))
        if resp.ok:
            item['meta'] = json.loads(resp.text)
        
        return item


class TicketCategoriesPipeline(object):
    TICKET_CATEGORIES_URL = 'https://www.piaoniu.com/api/v1/ticketCategories.json?b2c=true&eventId={}'

    def process_item(self, item, spider):
        events = item['meta']['events']
        item['ticket_categories'] = [] # initialize ticket categories 

        for event in events:
            resp = requests.get(self.TICKET_CATEGORIES_URL.format(event['id']))

            if resp.ok:
                item['ticket_categories'] += json.loads(resp.text) # concatenate if necessary
        
        return item


class TicketPipeline(object):
    TICKET_URL = 'https://www.piaoniu.com/api/v4/tickets.json?b2c=true&eventId={}&ticketCategoryId={}'

    def process_item(self, item, spider):
        item['tickets'] = {}
        ticket_categories = item['ticket_categories']

        for c in ticket_categories:
            resp = requests.get(self.TICKET_URL.format(c['activityEventId'], c['id']))

            if resp.ok:
                item['tickets'][c['id']] = json.loads(resp.text)
        
        return item