# -*- coding: utf-8 -*-
import scrapy
import json

class DamaiSpider(scrapy.Spider):
    name = 'damai'
    allowed_domains = ['damai.cn']
    start_urls = ['https://search.damai.cn/searchajax.html?cty=上海']

    def parse(self, response):
        r = json.loads(response.text)
        page = r['pageData']

        if page.get('resultData'):
            for r in page['resultData']:
                project_id = r['projectid']
                l = len(str(project_id))
            
                if l <= 8: 
                    url = 'https://piao.damai.cn/ajax/getInfo.html?projectId={}'.format(project_id)
                    yield scrapy.Request(url=url, callback=self.parse_piao)
                elif l >= 9 and l <= 11:
                    url = 'https://item.damai.cn/item/project.htm?id={}'.format(project_id)
                    yield scrapy.Request(url=url, callback=self.parse_item)
                else:
                    url = 'https://detail.damai.cn/item.htm?id={}'.format(project_id)
                    yield scrapy.Request(url=url, callback=self.parse_detail)                

        if page['currentPage'] != page['nextPage']:
            yield response.follow(url=self.start_urls[0] + '&currPage={}'.format(page['nextPage']), callback=self.parse)

    def parse_item(self, response):
        # haven't found an example
        pass

    def parse_piao(self, response):
        r = json.loads(response.text)

        if r['Status'] == 200:
            yield r['Data']

    def parse_detail(self, response):
        performance = json.loads(response.css('div#dataDefault::text').get())
        static_info = json.loads(response.css('div#staticDataDefault::text').get())

        yield performance