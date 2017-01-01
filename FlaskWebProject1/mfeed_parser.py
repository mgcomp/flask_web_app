import feedparser
from bs4 import BeautifulSoup
from newspaper import Article


class mfeed_parser(object):
    """Feed parser"""
    @staticmethod
    def parse_summary(summary):
        soup = BeautifulSoup(summary);
        soup_text = soup.get_text(strip=True);
        return_data = {};
        return_data['text'] = soup_text;
        return_data['image'] = None;
        for mtag in soup.findAll("img"):
            print("Found img src =" + mtag['src'] + "->in summary:"+summary);
            return_data['image'] = mtag['src'];
            
        return return_data;

    @staticmethod
    def get_news(murl):
        feed = feedparser.parse(murl);
        feedlist = [];
        for post in feed.entries:
            title = post.title;
            summary_data = mfeed_parser.parse_summary(post.summary);
            summary = post.summary;
            post_url = post.link;
            feedlist.append({'title':title,'summary':summary_data['text'],'image_url':summary_data['image'],'url':post_url});
        
        res = {};
        res['url'] = murl;
        res['all_feeds'] = feedlist;
        return res;
    
    @staticmethod    
    def get_news_text_from_post(url):
        print("mfeed_parser:getting article text for:" +url);
        article = Article(url);
        article.download();
        article.parse();

        print("mfeed_parser:cleaned_text is:"+article.text);
        return article.text;
        
        
        


