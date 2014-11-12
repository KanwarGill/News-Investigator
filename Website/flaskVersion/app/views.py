from celery import Celery, task
from crawl import webcrawl
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
manager = CouchDBManager()
manager.setup(app)

'''
Celery tasks
'''
@task(name="tasks.add")
def add(x, y):
    return x + y
    
@task(name='tasks.start_crawl')
def start_crawl():
    return webcrawl()

'''
Web pages
'''
@app.route('/')
@app.route('/index')
def index_page():
    '''Return the index/home page.'''
    return render_template("index.html", title='Home')

@app.route("/test")
def test_page(x=16, y=16):
    '''Create a test celery task and return the task id.'''
    x = int(request.args.get("x", x))
    y = int(request.args.get("y", y))
    res = add.apply_async((x, y))
    context = {"id": res.task_id, "x": x, "y": y}
    result = "add((x){}, (y){})".format(context['x'], context['y'])
    goto = "{}".format(context['id'])
    return jsonify(result=result, goto=goto)

@app.route("/test/result/<task_id>")
def test_result_page(task_id):
    '''Show the result of the celery task, given the task id.'''
    retval = add.AsyncResult(task_id).get(timeout=1.0)
    return repr(retval)
    
@app.route('/crawl')
def crawl_page():
    '''Return the crawl page.'''
    return render_template("crawl.html", title='Crawl')

@app.route('/table')
def view_table_page():
    '''Return the table results page.'''
    return render_template("table.html", title='Crawl Results')

'''
GET/POST methods
''' 
@app.route('/crawling', methods=['POST'])
def crawling_task():
    '''Start the web crawl task. Return the task id of the task.'''
    res = start_crawl.apply_async()
    context = {"id": res.task_id}
    result = "start_crawl()"
    goto = "{}".format(context['id'])
    return jsonify(result=result, goto=goto)

@app.route('/add_source', methods=['POST'])
def add_source():
    '''TODO: Does not work at the moment, need to reconfigure database'''
    id = request.args.get("id", id)
    source = request.args.get("url", source)
    app.config.update(
        COUCHDB_DATABASE = 'news_source')
    manager.setup(app)
    # Error checking here
    document = dict(_id=id, source=source)
    g.couch[id] = document
    g.couch.save(document)
    return jsonify(id=id, source=source, result="good")
    
def delete_source():
    pass
    
def add_keywords():
    pass
    
def delete_keywords():
    pass

@app.route('/get_results', methods=['GET'])
def get_results():
    '''Return the results of the crawl in a JSON object.'''
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
        hyperlinks = re.findall(r'<a[^>]* href="([^"]*)"', row.value[source])
        # get all the quotes
        quotes = re.findall(r'"(?:[^"\\]|\\.)*"', row.value[source])
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
    
def retrieve_results(query):
    '''Return the results of the query from the database.'''
    return g.couch.query(query)
        
if __name__ == "__main__":
    # Run the web app on localhost:5000
    port = int(environ.get("PORT", 5000))
    app.run(host='localhost', port=port, debug=True)
