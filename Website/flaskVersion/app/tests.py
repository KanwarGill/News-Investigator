from mock import patch
from views import app

import json
import requests
import unittest


class FakeViewResults(object):
    '''A replicated couchdb.client.ViewResults object.'''
    def __init__(self, id, key, value):
        self.id = id
        self.key = key
        self.value = value
    

def db_stub(*args, **kwargs):
    value = {"_id":"44a18fd3d4f47c07557fe42843000836","_rev":"1-a57abce11486848c0b2f9d295544bf0e","date":"Tue, 11 Nov 2014 20:38:11 GMT","source":"<p>Iraqi soldiers battling the Islamic State of Iraq and the Levant (ISIL) have recaptured the heart of the town of Beiji, home to the country's largest oil refinery, according to state television and a military official.</p>","link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html","id":"al2","title":"Iraqi forces close in on major oil refinery"}
    response = [FakeViewResults("1234", "al2", value)]
    return response

class NewsInvestigatorTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    @patch('views.retrieve_results')
    def test_get_results(self, mock_db):
        # Use the stub instead of an actual query to the database
        mock_db.side_effect = db_stub
        result = self.app.get('/get_results')
        expected = [{'title':"Iraqi forces close in on major oil refinery", "date": "Tue, 11 Nov 2014 20:38:11 GMT", "link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html"}]
        result = json.loads(result.data)
        self.assertEquals(result, expected)

if __name__ == '__main__':
    unittest.main()