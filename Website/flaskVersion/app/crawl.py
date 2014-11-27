from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from webcrawl.spiders.article_spider import ArticleSpider
from webcrawl.spiders.feed_spider import FeedSpider
from scrapy.utils.project import get_project_settings

def article_crawl():
    spider = ArticleSpider()
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run() # the script will block here until the spider_closed signal was sent
    
def feed_crawl():
    spider = FeedSpider()
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run() # the script will block here until the spider_closed signal was sent