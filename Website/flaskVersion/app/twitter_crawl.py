import tweepy
from database import NewsInvestigatorDatabase
from flaskext.couchdb import CouchDBManager
import settings
import couchdb

couch = couchdb.Server('http://chihuahuas.iriscouch.com:5984/')
db = couch['test_news_investigator']


def twitter_crawl():
    # authentication for Twitter API
    auth = tweepy.OAuthHandler('PNIJuzLXezWr3xrxScEbA68l3', 
                        'Li7Z5ZOvIu4o50G0n2wEmv5Nj0JmsCvSjR7OUx4CMompnIqGjH')
    auth.set_access_token('64169290-OZeLtehY0eSBkj12ebWZlYP8KtzlJtxLF5DEM7Jb8', 
                          'WbgHw8xyDJ77ZqWKDjs9B2rzEKzAuHcBFrO04xB9bgNqo')
    
    # include the twitter authentication
    #auth = tweepy.OAuthHandler('XBuKUEBKUIkdWxsJGHapWZp2j', 
                            #'99xPfB2FJxzoDfjxd2Pz0aO6l4wMl7EvqL1osvvP8QpFNPLe9T')
    #auth.set_access_token('2891335167-8KtLExQ2JSqf1dAR1uo4P4Nnao54bXyQJX1RRA0', 
                          #'sUcWM6cx98GP4xuQagmJ6zQr2FoseqUppWnXSCdQbdUec')
    
    api = tweepy.API(auth)    
    page_num = 0
    num_of_tweets = 0
    handles_list = []
    keywords = []
    tweets = []
    ids = []
    
    # create the handles list
    for handle in db.view('byDocType/byHandle'):
	handles_list.append(handle.value['handle'])
	
    # loop through the list of handles and save the tweets in the database
    for handle in handles_list:
	# start from page 0 for each handle
	page_num = 0
	user_tweets = []
	# look at the first five pages of tweets for each handle
	while (page_num < 6):
	    for tweet in (api.user_timeline(handle, page=page_num)):
		user_tweets.append(tweet.text)
	    page_num += 1
	try:
	    # save the tweet in the database if it's a new ID
	    document = dict(_id="tweet_" + handle, doc_type="tweet", tweet=user_tweets)
	    db.save(document)
	    print "Document with id " + _id + "saved"
	except:
	    # otherwise update the existing ID
	    print "ID tweet_" + handle + " already exists"
	    document = dict(_id="tweet_" + handle, doc_type="tweet", tweet=user_tweets)
	    db.update([document])
	    print "Updated"