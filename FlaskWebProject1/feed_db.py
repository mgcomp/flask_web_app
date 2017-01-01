from FlaskWebProject1 import mfeed_parser

from datetime import datetime, timedelta
import os
import _pickle as cPickle

class feed_db(object):
    """Database of all feeds"""

    def __init__(self,feed_timeout_in_seconds):
        self.feed_database = {};
        self.timeout_delta = timedelta(seconds = feed_timeout_in_seconds);
    
    def get_feeds_for_urls(self,url_list):
        if url_list is None:
            return [];
        return [self.get_feed_for_url(url) for url in url_list];

    def get_feed_for_url(self,feed_url):
        current_time = datetime.now();
        if not self.__has_feed_in_local_db(feed_url,current_time):
            self.feed_database[feed_url] = mfeed_parser.mfeed_parser.get_news(feed_url);
            self.feed_database[feed_url]['fetch_time'] = current_time;
        
        return self.feed_database[feed_url];


    def __has_feed_in_local_db(self,feed_url,current_time):
        if feed_url not in self.feed_database.keys():
            print("feed_db: could not find in db:"+feed_url);
            return False;
        if (current_time - self.feed_database[feed_url]['fetch_time'])> self.timeout_delta:
            del self.feed_database[feed_url];
            print("feed_db: found in db, but too old:" +feed_url);
            return False;
        print ("feed_db: found fresh copy in db:" +feed_url);
        return True;
 
    def get_news_string_for_post(self,url):
        return mfeed_parser.mfeed_parser.get_news_text_from_post(url);

    def save_to_file(self,fname):
        print ("Feed db: writing to file:"+fname);
        with open(fname,"wb") as pickle_file:
            cPickle.dump(self.feed_database,pickle_file);

    def load_from_file(self,fname):
        if os.path.isfile(fname):
            print("Feed db: loading from file:"+fname);
            with open(fname,'rb') as pickle_file:
                self.feed_database = cPickle.load(pickle_file);        
        

