from flask import Flask, render_template, jsonify, request
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from webcrawl.spiders.aljazeera_spider2 import AlJazzera2Spider
from scrapy.utils.project import get_project_settings
import settings
from celery import Celery, task
from os import path, environ
from crawl import webcrawl

app = Flask(__name__)
app.config.from_object(settings)

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

celery = make_celery(app)

@task(name="tasks.add")
def add(x, y):
    return x + y
    
@app.route("/test")
def hello_world(x=16, y=16):
    x = int(request.args.get("x", x))
    y = int(request.args.get("y", y))
    res = add.apply_async((x, y))
    context = {"id": res.task_id, "x": x, "y": y}
    result = "add((x){}, (y){})".format(context['x'], context['y'])
    goto = "{}".format(context['id'])
    return jsonify(result=result, goto=goto)

@app.route("/test/result/<task_id>")
def show_result(task_id):
    retval = add.AsyncResult(task_id).get(timeout=1.0)
    return repr(retval)
    

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
    res = start_crawl.apply_async()
    context = {"id": res.task_id}
    result = "start_crawl()"
    goto = "{}".format(context['id'])
    return jsonify(result=result, goto=goto)
    
@task(name='tasks.start_crawl')
def start_crawl():
    return webcrawl()
    
@app.route("/result/<task_id>")
def show_crwal_result(task_id):
    retval = start_crawl.AsyncResult(task_id).get(timeout=1.0)
    return repr(retval)
    
if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host='localhost', port=port, debug=True)
