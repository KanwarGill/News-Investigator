from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from webcrawl.items import AlJazeeraItem
from scrapy.http import Request
import couchdb
from scrapy.conf import settings

class AlJazzera2Spider(CrawlSpider):
    start_urls = []
    
    # Access CouchDB database
    couch = couchdb.Server(settings['COUCHDB_SERVER'])
    db = couch[settings['NEWSSOURCE']]
    # Grab all urls from the news_source database
    for row in db.view('_all_docs'):
        #print row.id
        document = db.get(row.id)
        #print document
        print document.items()[0][1]
        start_urls.append(document.items()[0][1])
    
    name = "al2"
    allowed_domains = ["http://www.aljazeera.com/", "www.aljazeera.com"]
    #start_urls = [
        #"http://www.aljazeera.com/Services/Rss/?PostingId=2007731105943979989"
    #]

    def parse(self, response):
        for article in response.xpath('//channel/item'):
            item = AlJazeeraItem()
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
        item ["source"] = hxs.select('//td[@class="DetailedSummary"]/p').extract()
        
        # Extract hyperlinks, extract quotes, extract mentions here
        
        return item


