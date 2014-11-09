from flask import render_template, jsonify
from app import app
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from webcrawl.spiders.aljazeera_spider2 import FollowAllSpider
from scrapy.utils.project import get_project_settings

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)
                           
@app.route('/crawl')
def crawl():
    return render_template("crawl.html",
                           title='Crawl')

@app.route('/crawling', methods=['POST'])
def crawling():
    spider = FollowAllSpider(domain='scrapinghub.com')
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run() # the script will block here until the spider_closed signal was sent
    return jsonify({'result': 'Connected'})
