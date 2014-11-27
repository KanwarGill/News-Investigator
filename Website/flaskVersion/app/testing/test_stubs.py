from fakeviewresults import FakeViewResults
    
def db_stub_simple(*args, **kwargs):
    value = {"_id":"44a","_rev":"1-a57a","date":"Tue, 11 Nov 2014 20:38:11 GMT","source":"<p>Iraqi soldiers battling the Islamic State of Iraq and the Levant (ISIL) have recaptured the heart of the town of Beiji, home to the country's largest oil refinery, according to state television and a military official.</p>","link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html","id":"al2","title":"Iraqi forces close in on major oil refinery", "html":"something", "text":"something", "date_crawled":"Tue, 11 Nov 2014 20:38:11 GMT"}
    response = [FakeViewResults("1234", "al2", value)]
    return response
    
def db_stub_hyperlink(*args, **kwargs):
    '''Stub that contains a hyperlink.'''
    value = {"_id":"44a","_rev":"1-a57a","date":"Tue, 11 Nov 2014 20:38:11 GMT","source":"<p>Iraqi soldiers battling the Islamic State of Iraq and the Levant (ISIL) have recaptured the heart of the town of Beiji, home to the country's largest oil refinery, according to state television and a military official.</p><a href=\"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html\">Something</a>","link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html","id":"al2","title":"Iraqi forces close in on major oil refinery", "text":"something else", "html":"<a href=\"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html\">Something</a>","date_crawled":"Tue, 11 Nov 2014 20:38:11 GMT"}
    response = [FakeViewResults("1234", "al2", value)]
    return response
    
def db_stub_hyperlinks(*args, **kwargs):
    '''Stub that contains two hyperlinks.'''
    value = {"_id":"44a","_rev":"1-a57a","date":"11 Nov 2014","source":"something","html":"<a href=\"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html\">Something</a> <p>Iraqi soldiers battling the Islamic State of Iraq and the Levant (ISIL) have recaptured the heart of the town of Beiji, home to the country's largest oil refinery, according to state television and a military official.</p><a href=\"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html\">Something</a>","link":"www.aljazeera.com","id":"al2","title":"Iraqi forces close in on major oil refinery", "text":"something", "date_crawled":"Tue, 11 Nov 2014 20:38:11 GMT"}
    response = [FakeViewResults("1234", "al2", value)]
    return response
    
def db_stub_quote(*args, **kwargs):
    '''Stub that contains one quote.'''
    value = {"_id":"44a","_rev":"1-a57a","date":"Tue, 11 Nov 2014 20:38:11 GMT","source":"something","html":"<p>Iraqi soldiers battling the Islamic State of Iraq and the Levant (ISIL) have recaptured the heart of the town of Beiji, home to the country's largest oil refinery, according to state television and a \"military official\".</p>","link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html","id":"al2","title":"Iraqi forces close in on major oil refinery", "text":"\"military official\"", "date_crawled":"Tue, 11 Nov 2014 20:38:11 GMT"}
    response = [FakeViewResults("1234", "al2", value)]
    return response
    
def db_stub_quotes(*args, **kwargs):
    '''Stub that contains more than one quote.'''
    value = {"_id":"44a","_rev":"1-a57a","date":"Tue, 11 Nov 2014 20:38:11 GMT","source":"something", "text":"<p>Iraqi soldiers battling the Islamic State of Iraq and the Levant (ISIL) have \"recaptured\" the heart of the town of Beiji, home to the country's largest oil refinery, according to state television and a \"military official\".</p>","html":"something","link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html","id":"al2","title":"Iraqi forces close in on major oil refinery", "date_crawled":"Tue, 11 Nov 2014 20:38:11 GMT"}
    response = [FakeViewResults("1234", "al2", value)]
    return response
