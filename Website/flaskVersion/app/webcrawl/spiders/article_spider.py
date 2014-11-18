from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from ..items import ArticleItem
from scrapy.http import Request
import couchdb
import re
from urlparse import urlparse

class ArticleSpider(CrawlSpider):
    
    # List of the start URLs
    start_urls = []
    # List of the allowed domains
    #allowed_domains = []
    
    # Access CouchDB database
    couch = couchdb.Server('http://chihuahuas.iriscouch.com:5984/')
    db = couch['news_investigator']
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
                # add the new urls to the allowed domains
                #allowed_domains.append("http://www." + ".".join(n2))
                #allowed_domains.append("www." + ".".join(n2))
        else:
            #allowed_domains.append("http://" + parsed.path)
            #allowed_domains.append(parsed.path)
            continue
        #print allowed_domains
    
    name = "article"
    
    def parse(self, response):
        for article in response.xpath('//channel/item'):
            item = ArticleItem()
            # Grab the title and the link to the article
            item ["title"] = article.xpath("title/text()").extract()
            item ["link"] = article.xpath("link/text()").extract()
            item ["date"] = article.xpath("pubDate/text()").extract()
            
            link = item["link"][0]
            # Grab the source of the page by making another Request
            yield Request(link,callback = self.parse_link, meta = dict(item = item))
                
    def parse_link(self, response):
        self.log('Grabbing source from %s' % response.url)
        hxs = HtmlXPathSelector(response)
        item = response.meta.get('item')
        # The articles in Al Jazeera is under the td tag,
        # Detailed Summary class
        # item ["source"] = hxs.select('//td[@class="DetailedSummary"]/p').extract()
        item ["source"] = hxs.select('//p').extract()
        
        return item


