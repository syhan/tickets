import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tickets.spiders.moretickets import MoreTicketsSpider
from tickets.spiders.piaoniu import PiaoNiuSpider

process = CrawlerProcess(get_project_settings())
process.crawl(MoreTicketsSpider)
process.crawl(PiaoNiuSpider)
process.start()