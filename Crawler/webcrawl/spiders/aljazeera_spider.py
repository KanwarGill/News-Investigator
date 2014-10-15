import scrapy

from tutorial.items import AlJazeeraItem

class AlJazeeraSpider(scrapy.Spider):
    name = "aljazeera"
    allowed_domains = ["http://www.aljazeera.com/"]
    start_urls = [
        "http://www.aljazeera.com/Services/Rss/?PostingId=2007731105943979989"
    ]

    def parse(self, response):
        for sel in response.xpath('//channel/item'):
            item = AlJazeeraItem()
            item['title'] = sel.xpath('title/text()').extract()
            item['link'] = sel.xpath('link/text()').extract()
            yield item