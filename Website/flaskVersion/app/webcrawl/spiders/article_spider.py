from ..items import ArticleItem
from boilerpipe.extract import Extractor
from lxml import html
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

import couchdb
import re

class ArticleSpider(BaseSpider):
    name = "article"
    start_urls = []
    allowed_domains = []
    crawled_links = []
    
    # Access CouchDB database
    couch = couchdb.Server('http://chihuahuas.iriscouch.com:5984/')
    db = couch['test_news_investigator']
    
    # Grab all urls from the site
    for row in db.view('byDocType/bySite'):
        start_urls.append(row.key)
        
    for row in db.view('byDocType/byDomain'):
        allowed_domains.append(row.key)
        
    def parse(self, response):
        hxs = Selector(response)
        
        item = ArticleItem()
        item["title"] = hxs.xpath('//title/text()').extract()
        item["link"] = response.url
        item["source"] = hxs.xpath('//p').extract()
        
        extractor = Extractor(extractor='ArticleExtractor', url=item["link"])
        
        source = extractor.getHTML()
        item["text"] = extractor.getText()
        item["html"] = source
        
        page = html.fromstring(source)
        links = page.xpath("//p//a/@href")

        linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
        
        for link in links:
            if linkPattern.match(link) and not link in self.crawled_links:
                self.crawled_links.append(link)
                yield Request(link, self.parse)
        

        yield item