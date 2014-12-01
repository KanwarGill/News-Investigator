from mock import patch, MagicMock
from testing.test_stubs import *
from views import app, db

import json
import requests
import unittest

class GetResultsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.maxDiff = None
    
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_results_simple(self, mock_db):
        '''
        Basic get_results, without any hyperlinks or quotes to
        search for.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_simple
        result = self.app.get('/get_results')
        result = json.loads(result.data)
        
        expected = [{
            'row_number':1,
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html",
            "quotes":[],
            "hyperlinks":[]}]
        
        self.assertEquals(result[0]['row_number'], expected[0]['row_number'])
        self.assertEquals(result[0]['date_crawled'], expected[0]['date_crawled'])
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])
        
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_results_one_hyperlink(self, mock_db):
        '''
        The html has one hyperlink embedded in the article.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_hyperlink
        result = self.app.get('/get_results')
        result = json.loads(result.data)
        expected = [{
            'row_number':1,
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html",
            "quotes":[],
            "hyperlinks":["http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html"]}]
        
        self.assertEquals(result[0]['row_number'], expected[0]['row_number'])
        self.assertEquals(result[0]['date_crawled'], expected[0]['date_crawled'])
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])
        
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_results_one_hyperlink_clean(self, mock_db):
        '''
        The html has one hyperlink embedded in the article.
        The hyperlink has additional info ('?...') that is not needed
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_hyperlink_clean
        result = self.app.get('/get_results')
        result = json.loads(result.data)
        expected = [{
            'row_number':1,
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html",
            "quotes":[],
            "hyperlinks":["http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html"]}]
        
        self.assertEquals(result[0]['row_number'], expected[0]['row_number'])
        self.assertEquals(result[0]['date_crawled'], expected[0]['date_crawled'])
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])

    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_results_many_hyperlinks(self, mock_db):
        '''
        The article has many (2) hyperlinks embedded.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_hyperlinks
        result = self.app.get('/get_results')
        result = json.loads(result.data)
        expected = [{
            'row_number':1,
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "11 Nov 2014",
            "link":"www.aljazeera.com",
            "quotes":[],
            "hyperlinks":["http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html", "http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html"]}]
        
        self.assertEquals(result[0]['row_number'], expected[0]['row_number'])
        self.assertEquals(result[0]['date_crawled'], expected[0]['date_crawled'])
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])
        
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_results_one_quote(self, mock_db):
        '''
        The article has one quote embedded.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_quote
        result = self.app.get('/get_results')
        result = json.loads(result.data)
        expected = [{
            'row_number':1,
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html",
            "quotes":['"military official"'],
            "hyperlinks":[]}]
        
        self.assertEquals(result[0]['row_number'], expected[0]['row_number'])
        self.assertEquals(result[0]['date_crawled'], expected[0]['date_crawled'])
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])
        
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_results_one_quote_clean(self, mock_db):
        '''
        The article has one quote embedded that contains weird
        characters. These characters should be removed.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_quote_clean
        result = self.app.get('/get_results')
        result = json.loads(result.data)
        expected = [{
            'row_number':1,
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html",
            "quotes":['"military official"'],
            "hyperlinks":[]}]
        
        self.assertEquals(result[0]['row_number'], expected[0]['row_number'])
        self.assertEquals(result[0]['date_crawled'], expected[0]['date_crawled'])
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])
        
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_results_many_quotes(self, mock_db):
        '''
        The article has many (2) articles embedded.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_quotes
        result = self.app.get('/get_results')
        result = json.loads(result.data)
        expected = [{
            'row_number':1,
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html",
            "quotes":['"military official"', '"recaptured"'],
            "hyperlinks":[]}]
        
        self.assertEquals(result[0]['row_number'], expected[0]['row_number'])
        self.assertEquals(result[0]['date_crawled'], expected[0]['date_crawled'])
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])
        
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_results_multiple_results(self, mock_db):
        '''
        Basic get_results, without any hyperlinks or quotes to
        search for. Database has two results saved from the 
        crawl.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_multiple
        result = self.app.get('/get_results')
        result = json.loads(result.data)
        
        expected = [{
            'row_number':1,
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html",
            "quotes":[],
            "hyperlinks":[]
            }, {
            'row_number':2,
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html",
            "quotes":[],
            "hyperlinks":["http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html"]}]
        
        self.assertEquals(result[0]['row_number'], expected[0]['row_number'])
        self.assertEquals(result[0]['date_crawled'], expected[0]['date_crawled'])
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])
        
        self.assertEquals(result[1]['row_number'], expected[1]['row_number'])
        self.assertEquals(result[1]['date_crawled'], expected[1]['date_crawled'])
        self.assertEquals(result[1]['title'], expected[1]['title'])
        self.assertEquals(result[1]['date'], expected[1]['date'])
        self.assertEquals(result[1]['link'], expected[1]['link'])
        self.assertItemsEqual(result[1]['quotes'], expected[1]['quotes'])
        self.assertItemsEqual(result[1]['hyperlinks'], expected[1]['hyperlinks'])
        
class GetTweetsTestSuite(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.maxDiff = None
        
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_tweets_no_keywords(self, mock_db):
        '''
        No keywords are stored in the database.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_no_keywords_has_tweets
        result = self.app.get('/get_tweets')
        result = json.loads(result.data)
        
        expected = []
        
        self.assertItemsEqual(result, expected)
        
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_tweets_no_tweets(self, mock_db):
        '''
        No tweets are stored in the database.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_has_keywords_no_tweets
        result = self.app.get('/get_tweets')
        result = json.loads(result.data)
        
        expected = [{
            'keyword' : 'Ferguson',
            'tweets' : 0,
            'tweets text' : []
        }]
        
        self.assertEquals(result[0]['keyword'], expected[0]['keyword'])
        self.assertEquals(result[0]['tweets'], expected[0]['tweets'])
        self.assertItemsEqual(result[0]['tweets text'], expected[0]['tweets text'])
        
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_tweets_tweet_have_no_keywords(self, mock_db):
        '''
        Tweets do not contain the specified keywords.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_tweets_doesnt_contain_keywords
        result = self.app.get('/get_tweets')
        result = json.loads(result.data)
        
        expected = [{
            'keyword' : 'Ferguson',
            'tweets' : 0,
            'tweets text' : []
        }]
        
        self.assertEquals(result[0]['keyword'], expected[0]['keyword'])
        self.assertEquals(result[0]['tweets'], expected[0]['tweets'])
        self.assertItemsEqual(result[0]['tweets text'], expected[0]['tweets text'])
        
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_tweet_tweets_have_keyword(self, mock_db):
        '''
        Tweet does contain the specified keyword.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_tweets_does_contain_keyword
        result = self.app.get('/get_tweets')
        result = json.loads(result.data)
        
        expected = [{
            'keyword' : 'Ferguson',
            'tweets' : 1,
            'tweets text' : ['a list of strings dealing with Ferguson [@CNN]']
        }]
        
        self.assertEquals(result[0]['keyword'], expected[0]['keyword'])
        self.assertEquals(result[0]['tweets'], expected[0]['tweets'])
        self.assertItemsEqual(result[0]['tweets text'], expected[0]['tweets text'])
        
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_tweets_tweet_have_multiple_keywords(self, mock_db):
        '''
        Tweet does contain the specified keywords.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_tweets_does_contain_keywords
        result = self.app.get('/get_tweets')
        result = json.loads(result.data)
        
        expected = [{
            'keyword' : 'Ferguson',
            'tweets' : 1,
            'tweets text' : ['a list of strings dealing with Ferguson and ISIS [@CNN]']
        }, {
            'keyword' : 'ISIS',
            'tweets' : 1,
            'tweets text' : ['a list of strings dealing with Ferguson and ISIS [@CNN]']
        }]
        
        self.assertEquals(result[0]['keyword'], expected[0]['keyword'])
        self.assertEquals(result[0]['tweets'], expected[0]['tweets'])
        self.assertItemsEqual(result[0]['tweets text'], expected[0]['tweets text'])
        
        self.assertEquals(result[1]['keyword'], expected[1]['keyword'])
        self.assertEquals(result[1]['tweets'], expected[1]['tweets'])
        self.assertItemsEqual(result[1]['tweets text'], expected[1]['tweets text'])
        
    @patch('views.NewsInvestigatorDatabase.get_view')
    def test_get_tweets_tweet_have_multiple_keywords(self, mock_db):
        '''
        Tweets does contain the specified keywords.
        '''
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_multiple_tweets_does_contain_keywords
        result = self.app.get('/get_tweets')
        result = json.loads(result.data)
        
        expected = [{
            'keyword' : 'Ferguson',
            'tweets' : 2,
            'tweets text' : ['a list of strings dealing with Ferguson and ISIS [@CNN]', 'another list of strings dealing with Ferguson and ISIS [@BNN]']
        }, {
            'keyword' : 'ISIS',
            'tweets' : 2,
            'tweets text' : ['a list of strings dealing with Ferguson and ISIS [@CNN]', 'another list of strings dealing with Ferguson and ISIS [@BNN]']
        }]
        
        self.assertEquals(result[0]['keyword'], expected[0]['keyword'])
        self.assertEquals(result[0]['tweets'], expected[0]['tweets'])
        self.assertItemsEqual(result[0]['tweets text'], expected[0]['tweets text'])
        
        self.assertEquals(result[1]['keyword'], expected[1]['keyword'])
        self.assertEquals(result[1]['tweets'], expected[1]['tweets'])
        self.assertItemsEqual(result[1]['tweets text'], expected[1]['tweets text'])

if __name__ == '__main__':
    unittest.main()
