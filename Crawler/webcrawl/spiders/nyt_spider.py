import scrapy

from webcrawl.items import NewYorkTimesItem

class AlJazeeraSpider(scrapy.Spider):
    name = "nyt"
    allowed_domains = ["http://rss.nytimes.com"]
    start_urls = [
        "http://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml"
    ]

    def parse(self, response):
        for sel in response.xpath('//channel/item'):
            item = NewYorkTimesItem()
            item['title'] = sel.xpath('title/text()').extract()
            item['link'] = sel.xpath('link/text()').extract()
            yield item