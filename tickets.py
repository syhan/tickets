import scrapy
from scrapy.crawler import CrawlerProcess
from tickets.spiders.moretickets import MoreTicketsSpider
from tickets.spiders.piaoniu import PiaoNiuSpider

process = CrawlerProcess()
process.crawl(MoreTicketsSpider)
process.crawl(PiaoNiuSpider)
process.start()