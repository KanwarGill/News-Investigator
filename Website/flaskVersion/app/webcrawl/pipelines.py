# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import couchdb
import re
from scrapy.conf import settings
from scrapy import log
import datetime

class CouchDBPipeline(object):
    
    def __init__(self):
        # chihuahuas.iriscouch.com
        couch = couchdb.Server(settings['COUCHDB_SERVER'])
        self.db = couch[settings['COUCHDB_DB']]
        self.keyword_db = couch[settings['KEYWORDS']]
        self.keywords = []
        # Grab all keywords from the keywords database
        for row in self.keyword_db.view('_all_docs'):
            document = self.keyword_db.get(row.id)
            # add the keywords to the list
            self.keywords.append(document.items()[2][1])
        print self.keywords

    def process_item(self, item, spider):

        # join the keywords from the list with or to facilitate regex
        keywords = "|".join(self.keywords)
        print "Keywords: ", keywords
        
        print "Title: ", item["title"]
        
        # join the strings in the source to create one giant string
        source = " ".join(item["source"])
        source = source.encode('ascii', 'ignore')
        #try:
            #spurce = source.decode(parsed_feed.encoding).encode('ascii', 'xmlcharrefreplace')
        #except UnicodeDecodeError:
            #print "UnicodeDecodeError"
        print "Source: ", source
        
        # parse the source to to see if it contains the keyword
        pattern = re.compile(keywords)
        m = pattern.search(source)
        if (m):
            print "Match found: ", m.group(), "in source ", source
            # create a dictionary with the name, title, link, and the source 
            # from the spider
            data = dict([('id', spider.name), ('title', item["title"][0]), 
                         ('link', item["link"][0]), 
                         ('source', source), ('date', item["date"][0])])
    
            self.db.save(data)
            log.msg("Item wrote to CouchDB database %s/%s" %
                        (settings['COUCHDB_SERVER'], settings['COUCHDB_DB']),
                        level=log.DEBUG, spider=spider)             
        else:
            print "No Match"
       
        return item