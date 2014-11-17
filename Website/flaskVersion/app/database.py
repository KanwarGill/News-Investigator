from flask import g
from flaskext.couchdb import CouchDBManager

class NewsInvestigatorDatabase(object):

    def __init__(self, app):
        self._manager = CouchDBManager()
        self._manager.setup(app)
        
    def save_document(self, id, document):
        g.couch[id] = document
        g.couch.save(document)
        
    def retrieve_results(self, query):
        return g.couch.query(query)
        
    def get_view(self, name):
        return g.couch.view(name)