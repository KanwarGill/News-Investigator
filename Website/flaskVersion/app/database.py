from flask import g
from flaskext.couchdb import CouchDBManager

class NewsInvestigatorDatabase(object):
    '''A NewsInvestigatorDatabase object.'''

    def __init__(self, app):
        '''
        Create a new NewsInvestigator object, with the given 
        Flask app settings.
        '''
        self._manager = CouchDBManager()
        self._manager.setup(app)
        
    def _save_document(self, id, document, doc_type):
        '''
        Save the document into the database.
        '''
        document['doc_type'] = doc_type
        g.couch[id] = document
        g.couch.save(document)
        
    def retrieve_results(self, query):
        '''
        Retrieve the results of a user generated query.
        '''
        return g.couch.query(query)
        
    def get_view(self, name):
        '''
        Grab the results of a predefined view.
        '''
        return g.couch.view(name)
        
    def save_news_source(self, id, document):
        '''
        Save a news source to the database.
        '''
        self._save_document('news_source_' + id, document, 'news_source')
        
    def save_keyword(self, id, document):
        '''
        Save a keyword to the database.
        '''
        self._save_document('keyword_' + id, document, 'keyword')
        
    def save_handle(self, id, document):
        '''
        Save a handle to the database.
        '''
        self._save_document('handle_' + id, document, 'handle')
        
    def save_tweet(self, id, document):
        '''
        Save a tweet to the database.
        '''
        self._save_document('tweet_' + id, document, 'tweet')
        
    def save_site(self, id, document):
        '''
        Save a site to the database.
        '''
        self._save_document('site_' + id, document, 'site')
        
    def save_domain(self, id, document):
        '''
        Save a domain to the database.
        '''
        self._save_document('domain_' + id, document, 'domain')
        
    def delete_document(self, id):
        '''
        Delete a document, given the id.
        '''
        document = g.couch[id]
        g.couch.delete(document)