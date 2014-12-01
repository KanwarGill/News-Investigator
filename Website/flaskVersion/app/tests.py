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
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html",
            "quotes":[],
            "hyperlinks":[]}]
        
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
        expected = [{
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html",
            "quotes":[],
            "hyperlinks":["http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html"]}]
        result = json.loads(result.data)
        
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
        expected = [{
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html",
            "quotes":[],
            "hyperlinks":["http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html"]}]
        result = json.loads(result.data)
        
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
        expected = [{
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "11 Nov 2014",
            "link":"www.aljazeera.com",
            "quotes":[],
            "hyperlinks":["http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html", "http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html"]}]
        result = json.loads(result.data)
        
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
        expected = [{
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html",
            "quotes":['"military official"'],
            "hyperlinks":[]}]
        result = json.loads(result.data)
        
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
        expected = [{
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html",
            "quotes":['"military official"'],
            "hyperlinks":[]}]
        result = json.loads(result.data)
        
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
        expected = [{
            'date_crawled':'Tue, 11 Nov 2014 20:38:11 GMT',
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html",
            "quotes":['"military official"', '"recaptured"'],
            "hyperlinks":[]}]
        result = json.loads(result.data)
        
        self.assertEquals(result[0]['date_crawled'], expected[0]['date_crawled'])
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])

if __name__ == '__main__':
    unittest.main()
