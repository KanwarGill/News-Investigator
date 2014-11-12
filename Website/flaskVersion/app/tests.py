from mock import patch
from testing.test_stubs import *
from views import app

import json
import requests
import unittest

class GetResultsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.maxDiff = None
    
    @patch('views.retrieve_results')
    def test_get_results_simple(self, mock_db):
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_simple
        result = self.app.get('/get_results')
        expected = [{
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html",
            "quotes":[],
            "hyperlinks":[]}]
        result = json.loads(result.data)
        
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])
        
    @patch('views.retrieve_results')
    def test_get_results_one_hyperlink(self, mock_db):
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_hyperlink
        result = self.app.get('/get_results')
        expected = [{
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html",
            "quotes":[],
            "hyperlinks":["http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html"]}]
        result = json.loads(result.data)
        
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])

    @patch('views.retrieve_results')
    def test_get_results_many_hyperlinks(self, mock_db):
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_hyperlinks
        result = self.app.get('/get_results')
        expected = [{
            'title':"Iraqi forces close in on major oil refinery",
            "date": "11 Nov 2014",
            "link":"www.aljazeera.com",
            "quotes":[],
            "hyperlinks":["http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html", "http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html"]}]
        result = json.loads(result.data)
        
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])
        
    @patch('views.retrieve_results')
    def test_get_results_one_quote(self, mock_db):
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_quote
        result = self.app.get('/get_results')
        expected = [{
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html",
            "quotes":['"military official"'],
            "hyperlinks":[]}]
        result = json.loads(result.data)
        
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])
        
    @patch('views.retrieve_results')
    def test_get_results_many_quotes(self, mock_db):
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub_quotes
        result = self.app.get('/get_results')
        expected = [{
            'title':"Iraqi forces close in on major oil refinery",
            "date": "Tue, 11 Nov 2014 20:38:11 GMT",
            "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html",
            "quotes":['"military official"', '"recaptured"'],
            "hyperlinks":[]}]
        result = json.loads(result.data)
        
        self.assertEquals(result[0]['title'], expected[0]['title'])
        self.assertEquals(result[0]['date'], expected[0]['date'])
        self.assertEquals(result[0]['link'], expected[0]['link'])
        self.assertItemsEqual(result[0]['quotes'], expected[0]['quotes'])
        self.assertItemsEqual(result[0]['hyperlinks'], expected[0]['hyperlinks'])

if __name__ == '__main__':
    unittest.main()