from ..items import ArticleItem
from boilerpipe.extract import Extractor
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy import Selector
from urlparse import urlparse

import couchdb
import re

class FeedSpider(CrawlSpider):

    name = "feed"
    # List of the start URLs
    start_urls = []
    
    # Access CouchDB database
    couch = couchdb.Server('http://cscc01-team16.iriscouch.com:5984/')
    db = couch['p4_test_news_investigator']
    # Grab all urls from the news_source database
    for row in db.view('byDocType/byNewsSource'):
        parsed = urlparse(row.key)
        # append the urls
        start_urls.append(row.key)
        # append the allowed domains
        if parsed.netloc:
            # if the url begins with rss, replace it with www
            if re.match('rss\..*\..*', parsed.netloc):
                new = parsed.netloc.encode("ascii", "ignore")
                n2 = new.split('.')
                # remove the rss item
                n2.pop(0)
    

    
    def parse(self, response):
        for article in response.xpath('//channel/item'):
            item = ArticleItem()
            # Grab the title and the link to the article
            item ["title"] = article.xpath("title/text()").extract()
            item ["link"] = article.xpath("link/text()").extract()
            item ["date"] = article.xpath("pubDate/text()").extract()
            
            link = item["link"][0]
            
            extractor = Extractor(extractor='ArticleExtractor', 
                    url=link)
            item ["text"] = extractor.getText()
            item ["html"] = extractor.getHTML()
            # Grab the source of the page by making another Request
            yield Request(link,callback = self.parse_link, meta = dict(item = item))
                
    def parse_link(self, response):
        self.log('Grabbing source from %s' % response.url)
        hxs = Selector(response)
        item = response.meta.get('item')
        # The articles in Al Jazeera is under the td tag,
        # Detailed Summary class
        # item ["source"] = hxs.select('//td[@class="DetailedSummary"]/p').extract()
        item ["source"] = hxs.xpath('//p').extract()
        
        return item


