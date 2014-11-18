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
        
    
    '''Process each crawled object and save it to the news_investigator database'''
    def process_item(self, item, spider):

        # join the keywords from the list with or to facilitate regex
        keywords = "|".join(self.keywords)
        
        # join the strings in the source to create one giant string
        # and change the encoding to ascii
        source = " ".join(item["source"])
        source = source.encode("ascii", "ignore")
        
        # parse the source to to see if it contains the keyword
        pattern = re.compile(keywords)
        m = pattern.search(source)
        if (m):
            print "Match found: ", m.group(), "in source ", source
            # create a dictionary with the name, title, link, and the source 
            # from the spider
            data = dict([("id", "results_" + spider.name), ("title", item["title"][0]), 
                         ("link", item["link"][0]), ("doc_type", "results"), 
                         ("source", source), ("date", item["date"][0])])
    
            self.db.save(data)
            log.msg("Item wrote to CouchDB database %s/%s" %
                        (settings["COUCHDB_SERVER"], settings["COUCHDB_DB"]),
                        level=log.DEBUG, spider=spider)             
        else:
            print "No Match"
       
        return item