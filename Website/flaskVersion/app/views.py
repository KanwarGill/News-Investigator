from celery import Celery, task
from crawl import webcrawl
from database import NewsInvestigatorDatabase
from flask import Flask, render_template, jsonify, request, g
from flaskext.couchdb import CouchDBManager
from os import path, environ

import tweepy
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

@task(name='tasks.start_crawl')
def start_crawl():
    '''Add the crawl task into the task queue.'''
    return webcrawl()

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

@app.route('/crawl')
def crawl_page():
    '''Return the crawl page.'''    
    return render_template('crawl.html', title='Crawl')

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

'''
GET/POST methods
''' 

@app.route('/crawling', methods=['POST'])
def crawling_task():
    '''Start the web crawl task. Return the task id of the task.'''
    res = start_crawl.apply_async()
    context = {"id": res.task_id}
    result = 'start_crawl()'
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

@app.route('/delete_source', methods=['POST'])    
@app.route('/delete_keyword', methods=['POST'])
@app.route('/delete_handle', methods=['POST'])
def delete_doc():
    '''Delete a document, given the id.'''
    id = request.form['id']
    db.delete_document(id)
    return jsonify(status='good')


@app.route('/get_results', methods=['GET'])
def get_results():
    '''Return the results of the crawl in a JSON object.'''
    results = []
    # Query the database for the documents
    q_results = db.get_view('byDocType/byResults')
    for row in q_results:
        # get all the hyperlinks
        hyperlinks = re.findall(r'<a[^>]* href="([^"]*)"', row.value['source'])
        # get all the quotes
        quotes = re.findall(r'"(?:[^"\\]|\\.)*"', row.value['source'])
        quotes_modified = []
        # modify the quotes to remove false positives
        for i in range(len(quotes)):
            if re.match(r'.*(=|_|<|>|http|internallink).*', quotes[i]):
                continue
            else:
                quotes_modified.append(quotes[i])         
        datarow = {
            'title': row.value['title'],
            'link': row.value['link'],
            'date': row.value['date'],
            'hyperlinks': hyperlinks,
            'quotes': quotes_modified
        }
        results.append(datarow)
    # Return the results as a JSON list
    return json.dumps(results)

@app.route('/get_tweets', methods=['GET'])
def get_tweets():
    
    # results list which will go in the twitter table
    results = []
    
    # authentication for Twitter API
    auth = tweepy.OAuthHandler('PNIJuzLXezWr3xrxScEbA68l3', 
                        'Li7Z5ZOvIu4o50G0n2wEmv5Nj0JmsCvSjR7OUx4CMompnIqGjH')
    auth.set_access_token('64169290-OZeLtehY0eSBkj12ebWZlYP8KtzlJtxLF5DEM7Jb8', 
                          'WbgHw8xyDJ77ZqWKDjs9B2rzEKzAuHcBFrO04xB9bgNqo')
    
    api = tweepy.API(auth)    

    num_of_tweets = 0
    handles_list = []
    keywords = []
    tweets = []
    for keyword in db.get_view('byDocType/byKeyword'):
        keywords.append(keyword.value['keyword'])
    
    # create the handles list
    for handle in db.get_view('byDocType/byHandle'):
        handles_list.append(handle.value['handle'])
                       
    # loop over the keywords
    for keyword in keywords:
        num_of_tweets = 0
        tweets = []
        for handle in handles_list:
            # get the tweets for the current handle and loop over them to 
            # see if it contains the keyword
            user_tweets = api.user_timeline(handle)
            for tweet in user_tweets:
                # if the tweet contains the keyword increment the number
                if re.match(keyword, tweet.text):
                    num_of_tweets += 1
                    tweets.append(tweet.text + ' [' + handle + ']\n')
        datarow = {
            'keyword': keyword,
            'tweets': num_of_tweets,
			'tweets text': tweets
        }
        results.append(datarow)
    
    #keywords = db.get_view('byDocType/byHandle')
    #for row in keywords:
        ##print "Line 199" + row
        #datarow = {
            #'handle': row.value['handle']
        #}
        #results.append(datarow)
    return json.dumps(results)

 
if __name__ == "__main__":
    # Run the web app on localhost:5000
    port = int(environ.get("PORT", 5000))
    # Not fixing the host name makes it run a bit better on mathlab
    app.run(port=port, debug=True)
