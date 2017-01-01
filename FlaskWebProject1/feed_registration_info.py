import os
import _pickle as cPickle

class feed_registration_info(object):
    def __init__(self):
        self.user_db_map = {};
        
    def add_feed(self,user,url):
        if user not in self.user_db_map.keys():
            self.user_db_map[user] = [];
        self.user_db_map[user].append(url);
    
    def get_feed_list(self,user):
        if user in self.user_db_map.keys():
            return self.user_db_map[user];
        return [];
    
    def save_to_file(self,fname):
        print("db_feed_info: writing to file:" + fname);
        with open(fname,'wb') as pickle_file:
            cPickle.dump(self.user_db_map,pickle_file);
    
    def load_from_file(self,fname):
        if os.path.isfile(fname):
            print("db_feed_info: loading from file:"+fname);
            with open(fname,'rb') as pickle_file:
                self.user_db_map = cPickle.load(pickle_file);
        