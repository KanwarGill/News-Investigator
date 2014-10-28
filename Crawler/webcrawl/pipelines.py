# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import couchdb
from scrapy.conf import settings
from scrapy import log
import datetime

class CouchDBPipeline(object):
    def __init__(self):
        # chihuahuas.iriscouch.com
        couch = couchdb.Server(settings['COUCHDB_SERVER'])
        self.db = couch[settings['COUCHDB_DB']]

    def process_item(self, item, spider):
        # create a dictionary with the name, title, link, and the source from the spider
        data = dict([('id', spider.name), ('title', item["title"]), 
                     ('link', item["link"]), ('date', item["date"]), 
                     ('source', item["source"])])

        self.db.save(data)
        log.msg("Item wrote to CouchDB database %s/%s" %
                    (settings['COUCHDB_SERVER'], settings['COUCHDB_DB']),
                    level=log.DEBUG, spider=spider)  
        return item
