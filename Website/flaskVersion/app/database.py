from flask import g
from flaskext.couchdb import CouchDBManager

class NewsInvestigatorDatabase(object):

    def __init__(self, app):
        self._manager = CouchDBManager()
        self._manager.setup(app)
        
    def _save_document(self, id, document, doc_type):
        document['doc_type'] = doc_type
        g.couch[id] = document
        g.couch.save(document)
        
    def retrieve_results(self, query):
        return g.couch.query(query)
        
    def get_view(self, name):
        return g.couch.view(name)
        
    def save_news_source(self, id, document):
        self._save_document('news_source_' + id, document, 'news_source')
        
    def save_keyword(self, id, document):
        self._save_document('keyword_' + id, document, 'keyword')