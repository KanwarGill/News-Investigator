from fakeviewresults import FakeViewResults
    
def db_stub_simple(*args, **kwargs):
    value = {"_id":"44a","_rev":"1-a57a","date":"Tue, 11 Nov 2014 20:38:11 GMT","source":"<p>Iraqi soldiers battling the Islamic State of Iraq and the Levant (ISIL) have recaptured the heart of the town of Beiji, home to the country's largest oil refinery, according to state television and a military official.</p>","link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html","id":"al2","title":"Iraqi forces close in on major oil refinery", "html":"something", "text":"something", "date_crawled":"Tue, 11 Nov 2014 20:38:11 GMT"}
    response = [FakeViewResults("1234", "al2", value)]
    return response
    
def db_stub_multiple(*args, **kwargs):
    response = []
    response.append(db_stub_simple()[0])
    response.append(db_stub_hyperlink()[0])
    return response
    
def db_stub_hyperlink(*args, **kwargs):
    '''Stub that contains a hyperlink.'''
    value = {"_id":"44a","_rev":"1-a57a","date":"Tue, 11 Nov 2014 20:38:11 GMT","source":"<p>Iraqi soldiers battling the Islamic State of Iraq and the Levant (ISIL) have recaptured the heart of the town of Beiji, home to the country's largest oil refinery, according to state television and a military official.</p><a href=\"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html\">Something</a>","link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html","id":"al2","title":"Iraqi forces close in on major oil refinery", "text":"something else", "html":"<a href=\"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html\">Something</a>","date_crawled":"Tue, 11 Nov 2014 20:38:11 GMT"}
    response = [FakeViewResults("1234", "al2", value)]
    return response
    
def db_stub_hyperlink_clean(*args, **kwargs):
    '''Stub that contains a hyperlink that needs to be cleaned.'''
    value = {"_id":"44a","_rev":"1-a57a","date":"Tue, 11 Nov 2014 20:38:11 GMT","source":"<p>Iraqi soldiers battling the Islamic State of Iraq and the Levant (ISIL) have recaptured the heart of the town of Beiji, home to the country's largest oil refinery, according to state television and a military official.</p><a href=\"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html?action=true&search=something+else\">Something</a>","link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html","id":"al2","title":"Iraqi forces close in on major oil refinery", "text":"something else", "html":"<a href=\"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji-20141111131541430331.html\">Something</a>","date_crawled":"Tue, 11 Nov 2014 20:38:11 GMT"}
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
    
def db_stub_quote_clean(*args, **kwargs):
    '''Stub that contains one quote that has weird characters.'''
    value = {"_id":"44a","_rev":"1-a57a","date":"Tue, 11 Nov 2014 20:38:11 GMT","source":"something","html":"<p>Iraqi soldiers battling the Islamic State of Iraq and the Levant (ISIL) have recaptured the heart of the town of Beiji, home to the country's largest oil refinery, according to state television and a \"military&#160; official***\".</p>","link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html","id":"al2","title":"Iraqi forces close in on major oil refinery", "text":"\"military official\"", "date_crawled":"Tue, 11 Nov 2014 20:38:11 GMT"}
    response = [FakeViewResults("1234", "al2", value)]
    return response
    
def db_stub_quotes(*args, **kwargs):
    '''Stub that contains more than one quote.'''
    value = {"_id":"44a","_rev":"1-a57a","date":"Tue, 11 Nov 2014 20:38:11 GMT","source":"something", "text":"<p>Iraqi soldiers battling the Islamic State of Iraq and the Levant (ISIL) have \"recaptured\" the heart of the town of Beiji, home to the country's largest oil refinery, according to state television and a \"military official\".</p>","html":"something","link":"http://www.aljazeera.com/news/middleeast/2014/11/iraqi-forces-close-beiji.html","id":"al2","title":"Iraqi forces close in on major oil refinery", "date_crawled":"Tue, 11 Nov 2014 20:38:11 GMT"}
    response = [FakeViewResults("1234", "al2", value)]
    return response

def db_stub_no_keywords_has_tweets(*args, **kwargs):
    ''''''
    if args[0] == "byDocType/byKeyword":
        return []
    elif args[0] == "byDocType/byTweet":
        value = {
            "_id":"tweet_@CNN",
            "_rev":"1-7ef78fd07f4e5e99af159d3b7a79993a",
            "doc_type":"tweet",
            "tweet":"a list of strings"}
        return [FakeViewResults("tweet_@CNN", "a list of strings", value)]
    else:
        return "Error"
        
def db_stub_has_keywords_no_tweets(*args, **kwargs):
    ''''''
    if args[0] == "byDocType/byKeyword":
        value = {
            "_id":"keyword_Ferguson",
            "_rev":"2-00e2430594e0cb76f562c9a598daa539",
            "doc_type":"keyword",
            "keyword":"Ferguson"}
        return [FakeViewResults("keyword_Ferguson", "Ferguson", value)]
    elif args[0] == "byDocType/byTweet":
        return []
    else:
        return "Error"
        
def db_stub_tweets_doesnt_contain_keywords(*args, **kwargs):
    ''''''
    if args[0] == "byDocType/byKeyword":
        value = {
            "_id":"keyword_Ferguson",
            "_rev":"2-00e2430594e0cb76f562c9a598daa539",
            "doc_type":"keyword",
            "keyword":"Ferguson"}
        return [FakeViewResults("keyword_Ferguson", "Ferguson", value)]
    elif args[0] == "byDocType/byTweet":
        value = {
            "_id":"tweet_@CNN",
            "_rev":"1-7ef78fd07f4e5e99af159d3b7a79993a",
            "doc_type":"tweet",
            "tweet":"a list of strings"}
        return [FakeViewResults("tweet_@CNN", "a list of strings", value)]
    else:
        return "Error"
        
def db_stub_tweets_does_contain_keyword(*args, **kwargs):
    ''''''
    if args[0] == "byDocType/byKeyword":
        value = {
            "_id":"keyword_Ferguson",
            "_rev":"2-00e2430594e0cb76f562c9a598daa539",
            "doc_type":"keyword",
            "keyword":"Ferguson"}
        return [FakeViewResults("keyword_Ferguson", "Ferguson", value)]
    elif args[0] == "byDocType/byTweet":
        value = {
            "_id":"tweet_@CNN",
            "_rev":"1-7ef78fd07f4e5e99af159d3b7a79993a",
            "doc_type":"tweet",
            "tweet":["a list of strings dealing with Ferguson"]}
        return [FakeViewResults("tweet_@CNN", "a list of strings dealing with Ferguson", value)]
    else:
        return "Error"
        
def db_stub_tweets_does_contain_keywords(*args, **kwargs):
    ''''''
    if args[0] == "byDocType/byKeyword":
        response = []
        value = {
            "_id":"keyword_Ferguson",
            "_rev":"2-00e2430594e0cb76f562c9a598daa539",
            "doc_type":"keyword",
            "keyword":"Ferguson"}
        response.append(FakeViewResults("keyword_Ferguson", "Ferguson", value))
        
        value = {
            "_id":"keyword_ISIS",
            "_rev":"2-00e2430594e0cb76f562c9a598daa539",
            "doc_type":"keyword",
            "keyword":"ISIS"}
            
        response.append(FakeViewResults("keyword_ISIS", "ISIS", value))
        
        return response
    elif args[0] == "byDocType/byTweet":
        value = {
            "_id":"tweet_@CNN",
            "_rev":"1-7ef78fd07f4e5e99af159d3b7a79993a",
            "doc_type":"tweet",
            "tweet":["a list of strings dealing with Ferguson and ISIS"]}
        return [FakeViewResults("tweet_@CNN", "a list of strings dealing with Ferguson and ISIS", value)]
    else:
        return "Error"
        
def db_stub_multiple_tweets_does_contain_keywords(*args, **kwargs):
    ''''''
    if args[0] == "byDocType/byKeyword":
        response = []
        value = {
            "_id":"keyword_Ferguson",
            "_rev":"2-00e2430594e0cb76f562c9a598daa539",
            "doc_type":"keyword",
            "keyword":"Ferguson"}
        response.append(FakeViewResults("keyword_Ferguson", "Ferguson", value))
        
        value = {
            "_id":"keyword_ISIS",
            "_rev":"2-00e2430594e0cb76f562c9a598daa539",
            "doc_type":"keyword",
            "keyword":"ISIS"}
            
        response.append(FakeViewResults("keyword_ISIS", "ISIS", value))
        
        return response
    elif args[0] == "byDocType/byTweet":
        response = []
        
        value = {
            "_id":"tweet_@CNN",
            "_rev":"1-7ef78fd07f4e5e99af159d3b7a79993a",
            "doc_type":"tweet",
            "tweet":["a list of strings dealing with Ferguson and ISIS"]}
        response.append(FakeViewResults("tweet_@CNN", "a list of strings dealing with Ferguson and ISIS", value))
        
        value = {
            "_id":"tweet_@BNN",
            "_rev":"1-7ef78fd07f4e5e99af159d3b7a79993a",
            "doc_type":"tweet",
            "tweet":["another list of strings dealing with Ferguson and ISIS"]}
        response.append(FakeViewResults("tweet_@BNN", "another list of tweets dealing with Ferguson and ISIS", value))
        
        return response
    else:
        return "Error"