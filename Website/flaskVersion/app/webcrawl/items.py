# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
    
class AlJazeeraItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()
    hyperlinks = scrapy.Field()
    date = scrapy.Field()
    # etc...
    
class NewYorkTimesItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
