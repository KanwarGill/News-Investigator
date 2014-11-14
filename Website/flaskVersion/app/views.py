from celery import Celery, task
from crawl import webcrawl
from flask import Flask, render_template, jsonify, request, g
from flaskext.couchdb import CouchDBManager
from os import path, environ

import re
import json
import requests
import settings

'''Return a celery object, given the app'''
def make_celery(app):
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
manager = CouchDBManager()
manager.setup(app)

'''
Celery tasks
'''

'''Add the crawl task into the task queue.'''
@task(name='tasks.start_crawl')
def start_crawl():
    return webcrawl()

'''
Web pages
'''

'''Return the index/home page.'''
@app.route('/')
@app.route('/index')
def index_page():
    return render_template('index.html', title='Home')

'''Return the crawl page.'''    
@app.route('/crawl')
def crawl_page():
    return render_template('crawl.html', title='Crawl')

'''Return the table results page.'''
@app.route('/table')
def view_table_page():
    return render_template('table.html', title='Crawl Results')

'''
GET/POST methods
''' 

'''Start the web crawl task. Return the task id of the task.'''
@app.route('/crawling', methods=['POST'])
def crawling_task():
    res = start_crawl.apply_async()
    context = {"id": res.task_id}
    result = 'start_crawl()'
    goto = '{}'.format(context['id'])
    return jsonify(result=result, goto=goto)

@app.route('/add_source', methods=['POST'])
def add_source():
    '''TODO: Does not work at the moment, need to reconfigure database'''
    id = request.args.get("id", id)
    source = request.args.get('url', source)
    app.config.update(
        COUCHDB_DATABASE = 'news_source')
    manager.setup(app)
    # Error checking here
    document = dict(_id=id, source=source)
    g.couch[id] = document
    g.couch.save(document)
    return jsonify(id=id, source=source, result='good')
    
def delete_source():
    pass
    
def add_keywords():
    pass
    
def delete_keywords():
    pass

'''Return the results of the crawl in a JSON object.'''
@app.route('/get_results', methods=['GET'])
def get_results():
    query = '''function(doc) {
        if (doc.id) {
            emit(doc.id, doc)
        }
    }
    '''
    results = []
    # Query the database for the documents
    q_results = retrieve_results(query)
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

'''Return the results of the query from the database.'''    
def retrieve_results(query):
    return g.couch.query(query)
 
if __name__ == "__main__":
    # Run the web app on localhost:5000
    port = int(environ.get("PORT", 5235))
    # Not fixing the host name makes it run a bit better on mathlab
    app.run(port=port, debug=True)
