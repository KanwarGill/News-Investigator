from celery import Celery, task
from crawl import webcrawl
from flask import Flask, render_template, jsonify, request
from flaskext.couchdb import CouchDBManager
from os import path, environ

import settings

# Initialize the web application
app = Flask(__name__)
app.config.from_object(settings)

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
    
# Create the celery task queue
celery = make_celery(app)

def make_db_manager(database):
    manager = CouchDBManager()
    COUCHDB_DATABASE = database
    manager.setup(app)
    return manager

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
    id = request.args.get("id", id)
    source = request.args.get("url", source)
    manager = make_db_manager('news_source')
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
    
def get_results():
    '''Return the results of the crawl.
    Possibly save it as a JSON file in /static/js/data1.json'''
    pass
    
if __name__ == "__main__":
    # Run the web app on localhost:5000
    port = int(environ.get("PORT", 5000))
    app.run(host='localhost', port=port, debug=True)
