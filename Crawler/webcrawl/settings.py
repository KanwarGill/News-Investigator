# -*- coding: utf-8 -*-

# Scrapy settings for webcrawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'webcrawl'

SPIDER_MODULES = ['webcrawl.spiders']
NEWSPIDER_MODULE = 'webcrawl.spiders'

ITEM_PIPELINES = {
    'webcrawl.pipelines.CouchDBPipeline': 300,
}

COUCHDB_SERVER = 'http://chihuahuas.iriscouch.com:5984/'
COUCHDB_DB = 'results'
NEWSSOURCE = 'news_source'
KEYWORDS = 'keywords'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'webcrawl (+http://www.yourdomain.com)'
