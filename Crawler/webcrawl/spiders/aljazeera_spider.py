import scrapy

from webcrawl.items import AlJazeeraItem

class AlJazeeraSpider(scrapy.Spider):
    name = "aljazeera"
    allowed_domains = ["http://www.aljazeera.com/"]
    start_urls = [
        "http://www.aljazeera.com/news/middleeast/2014/10/isil-launches-fierce-new-assault-kobane-201410219413238741.html"
    ]

    def parse(self, response):
        for sel in response.xpath('//td[@class="DetailedSummary"]'):
            item = AlJazeeraItem()
            #item['title'] = sel.xpath('title/text()').extract()
            item['link'] = sel.xpath('p/text()').extract()
            self.log(item['link'])
            yield item