from celery import Celery, task
from crawl import article_crawl, feed_crawl
from twitter_crawl import twitter_crawl
from database import NewsInvestigatorDatabase
from flask import Flask, render_template, jsonify, request, g
from flaskext.couchdb import CouchDBManager
from os import path, environ

import re
import json
import requests
import settings


def make_celery(app):
    '''Return a celery object, given the app'''
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

# Initialize the web application
app = Flask(__name__)
app.config.from_object(settings)

# Create the celery task queue
celery = make_celery(app)

# Setup database
db = NewsInvestigatorDatabase(app)

'''
Celery tasks
'''

@task(name='tasks.start_article_crawl')
def start_article_crawl():
    '''Add the article crawl task into the task queue.'''
    return article_crawl()
    
@task(name='tasks.start_feed_crawl')
def start_feed_crawl():
    '''Add the feed crawl task into the task queue.'''
    return feed_crawl()

@task(name='tasks.start_twitter_crawl')
def start_twitter_crawl():
    '''Add the crawl task into the task queue.'''
    return twitter_crawl()

'''
Web pages
'''

@app.route('/')
@app.route('/login')
def login():
    '''Return the login page.'''
    return render_template('login.html', title='Login Page')

@app.route('/index')
def index_page():
    '''Return the index/home page.'''
    return render_template('index.html', title='Home')

@app.route('/feed_crawl')
def crawl_page():
    '''Return the crawl page.'''
    return render_template('crawl.html', title='Feed Crawl')

@app.route('/twitter_crawl')
def twitter_crawl_page():
    '''Return the twitter crawl page.'''
    return render_template('twitter_crawl.html', title='Twitter Crawl')
    
@app.route('/table')
def view_table_page():
    '''Return the table results page.'''
    return render_template('table.html', title='Crawl Results')

@app.route('/twitter_table')
def view_twitter_table():
    '''Return the twitter table results page.'''
    return render_template('twitter_table.html', title='Twitter Results')

@app.route('/signup')
def signup():
    '''Return the sign up page.'''
    return render_template('signup.html', title='Sign Up Page')

@app.route('/forgotpassword')
def forgotpassword():
    '''Return the password recovery page.'''
    return render_template('forgotpassword.html', title='Forgot Password')

@app.route('/keywords')
def keywords_page():
    '''Return the keywords page.'''
    return render_template('keywords.html', title='Keywords')
    
@app.route('/article_crawl')
def article_crawl_page():
    '''Return the keywords page.'''
    return render_template('article_crawl.html', title='Article Crawl')

'''
GET/POST methods
''' 

@app.route('/article_crawling', methods=['POST'])
def article_crawling_task():
    '''Start the web crawl task. Return the task id of the task.'''
    res = start_article_crawl.apply_async()
    context = {"id": res.task_id}
    result = 'start_article_crawl()'
    return jsonify(status='started')

@app.route('/feed_crawling', methods=['POST'])
def feed_crawling_task():
    '''Start the web crawl task. Return the task id of the task.'''
    res = start_feed_crawl.apply_async()
    context = {"id": res.task_id}
    result = 'start_feed_crawl()'
    return jsonify(status='started')
    
@app.route('/twitter_crawling', methods=['POST'])
def twitter_task():
    '''Start the twitter crawl task. Return the task id of the task.'''
    result = twitter_crawl()
    return jsonify(status='started')
    
@app.route('/add_source', methods=['POST'])
def add_source():
    '''Add a news source to the database. Requires the id and url.'''
    id = request.form['id']
    url = request.form['url']
    document = dict(_id=id, url=url)
    db.save_news_source(id, document)
    return jsonify(id=id, url=url, status='good')

@app.route('/get_sources', methods=['GET'])
def get_sources():
    '''Return the list of news sources from the database.'''
    results = []
    for row in db.get_view('byDocType/byNewsSource'):
        results.append(row)
    return jsonify(data=results)

@app.route('/add_keyword', methods=['POST'])
def add_keyword():
    '''Add a keyword to the database. Requires the id and keyword.'''
    id = request.form['id']
    keyword = request.form['keyword']
    document = dict(_id=id, keyword=keyword)
    db.save_keyword(id, document)
    return jsonify(id=id, keyword=keyword, status='good')

@app.route('/get_keywords', methods=['GET'])
def get_keywords():
    '''Return the list of keywords from the database.'''
    results = []
    for row in db.get_view('byDocType/byKeyword'):
        results.append(row)
    return jsonify(data=results)

@app.route('/add_handle', methods=['POST'])
def add_handle():
    '''Add a handle to the database. Requires the id and the handle name.'''
    id = request.form['id']
    handle = request.form['handle']
    document = dict(_id=id, handle=handle)
    db.save_handle(id, document)
    return jsonify(id=id, handle=handle, status='good')

@app.route('/get_handles', methods=['GET'])
def get_handles():
    '''Return the list of handles from the database.'''
    results = []
    for row in db.get_view('byDocType/byHandle'):
        results.append(row)
    return jsonify(data=results)

@app.route('/add_site', methods=['POST'])
def add_site():
    '''Add a article site to the database. Requires the id and url.'''
    id = request.form['id']
    url = request.form['url']
    document = dict(_id=id, url=url)
    db.save_site(id, document)
    return jsonify(id=id, url=url, status='good')
    
@app.route('/get_sites', methods=['GET'])
def get_sites():
    '''Return the list of handles from the database.'''
    results = []
    for row in db.get_view('byDocType/bySite'):
        results.append(row)
    return jsonify(data=results)
    
@app.route('/add_domain', methods=['POST'])
def add_domain():
    '''Add a article site to the database. Requires the id and url.'''
    id = request.form['id']
    url = request.form['url']
    document = dict(_id=id, url=url)
    db.save_domain(id, document)
    return jsonify(id=id, url=url, status='good')
    
@app.route('/get_domains', methods=['GET'])
def get_domains():
    '''Return the list of handles from the database.'''
    results = []
    for row in db.get_view('byDocType/byDomain'):
        results.append(row)
    return jsonify(data=results)

@app.route('/delete_source', methods=['POST'])    
@app.route('/delete_keyword', methods=['POST'])
@app.route('/delete_handle', methods=['POST'])
@app.route('/delete_site', methods=['POST'])
@app.route('/delete_domain', methods=['POST'])
def delete_doc():
    '''Delete a document, given the id.'''
    id = request.form['id']
    db.delete_document(id)
    return jsonify(status='good')


@app.route('/get_results', methods=['GET'])
def get_results():
    '''Return the results of the crawl in a JSON object.'''
    results = []
    row_number = 0
    # Query the database for the documents
    q_results = db.get_view('byDocType/byResults')
    for row in q_results:
        row_number += 1
        # Get all the hyperlinks
        hyperlinks = re.findall(r'<[Aa][^>]* href="([^"]*)"', row.value['html'])
        # Clean the hyperlink by removing characters from ? onwards
        clean_hyperlinks = []
        for hyperlink in hyperlinks:
            i = hyperlink.find('?')
            if i > 0:
                clean_hyperlinks.append(hyperlink[:i])
            else:
                clean_hyperlinks.append(hyperlink)
        
        # get all the quotes
        quotes = re.findall(r'"(?:[^"\\]|\\.)*"', row.value['text'])
        quotes_modified = []
        # modify the quotes to remove false positives
        for i in range(len(quotes)):
            if re.match(r'.*(=|_|<|>|http|internallink).*', quotes[i]):
                continue
            else:
                # Clean the string to remove any special characters
                clean_quotes = re.sub('[^A-Za-z0-9\"\'\.\ \-\,\;\!\:]', '', quotes[i])
                quotes_modified.append(clean_quotes)         
        datarow = {
            'row_number': row_number,
            'date_crawled': row.value['date_crawled'],
            'title': row.value['title'],
            'link': row.value['link'],
            'date': row.value['date'],
            'hyperlinks': clean_hyperlinks,
            'quotes': quotes_modified
        }
        results.append(datarow)
    # Return the results as a JSON list
    return json.dumps(results)
 
@app.route('/get_tweets', methods=['GET'])
def get_tweets():
    '''Return the tweets of the twitter crawl in a JSON object'''
    
    # results list which will go in the twitter table
    results = []
    # list of keywords
    keywords = []
    # list of tweets
    tweets = []
    
    # add the keywords from the database in a list
    for keyword in db.get_view('byDocType/byKeyword'):
        keywords.append(keyword.value['keyword'])
	
    # loop over the keyowrds
    for keyword in keywords:
        # flush the number of tweets and tweets for each keyword
        num_of_tweets = 0
        tweets = []
        try:
            # get the tweets from the database
            for tweet in db.get_view('byDocType/byTweet'):
                # get the tweet handle excluding the string "tweet_"
                tweet_handle = tweet.value['_id'][6:] 
                # if the keyword is part of the tweet, then append it to tweets
                # and increment the number
                for t in tweet.value['tweet']:
                    if (keyword in t):
                        tweets.append(t + " [" + tweet_handle + "]")
                        num_of_tweets += 1	
        except:
            print "No documents of type tweet"

        datarow = {
        'keyword': keyword,
        'tweets': num_of_tweets,
        'tweets text': tweets
        }
        results.append(datarow)
	
    return json.dumps(results)

@app.route('/get_tweets_graph', methods=['GET'])
def get_tweets_graph():
    '''
    Return list keywords and tweet counts for them.
    Used for the twitter graph.
    '''
    
    keywords = []
    tweet_count = []
    
    # add the keywords from the database in a list
    for keyword in db.get_view('byDocType/byKeyword'):
        keywords.append(keyword.value['keyword'])
        
    for keyword in keywords:
        num_of_tweets = 0
        # get the tweets from the database
        for tweet in db.get_view('byDocType/byTweet'):
            # get the tweet handle excluding the string "tweet_"
            tweet_handle = tweet.value['_id'][6:] 
            # if the keyword is part of the tweet, then append it to tweets
            # and increment the number
            for t in tweet.value['tweet']:
                if (keyword in t):
                    num_of_tweets += 1	
        tweet_count.append(num_of_tweets)
    
    ret = dict(keyword=keywords, count=tweet_count)
    return jsonify(ret)

@app.route('/table_graph', methods=['GET'])
def table_graph():
    '''Return a list of dates to use, and a set of graph datasets'''
    articles = []
    quote_count = []
    link_count = []
    row_number = 0
    #grab results
    table = db.get_view('byDocType/byResults')
    for row in table:
        row_number += 1
        articles.append(row.value['title'][:10])
        #grab hyperlinks
        hyperlinks = re.findall(r'<[Aa][^>]* href="([^"]*)"', row.value['html'])
        #count links, add to link count dataset
        link_count.append(len(hyperlinks))
        #grab quotes
        quotes = re.findall(r'"(?:[^"\\]|\\.)*"', row.value['text'])
        quotes_modified = []
        # modify the quotes to remove false positives
        for i in range(len(quotes)):
            if re.match(r'.*(=|_|<|>|http|internallink).*', quotes[i]):
                continue
            else:
                quotes_modified.append(quotes[i])
        #count quotes, add to quote count dataset
        quote_count.append(len(quotes_modified))
        
    article_row = []
    for i in range(1, row_number+1):
        article_row.append("Article #" + str(i))

    graph_data = dict(article=articles, quotes=quote_count, links=link_count, row=article_row)

    return jsonify(graph_data)

if __name__ == "__main__":
    # Run the web app on localhost:5000
    port = int(environ.get("PORT", 5000))
    # Not fixing the host name makes it run a bit better on mathlab
    app.run(port=port, debug=True)
