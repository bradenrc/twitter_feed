#!/usr/bin/python

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time
from datetime import datetime, timedelta
import os
import pprint
#import elasticsearch
import HTMLParser


html_parser = HTMLParser.HTMLParser()

consumer_key="h9ZHlkz53jYPWFoxSZNoFtuf9"
consumer_secret="I4DEEOiNbR1OTO0UM5j5OsyLv7mcFAOySu6U4OHuVg85T0CpFm"
access_token="23088031-k7lxpDWd9o5lcqrnkjZfbNsVNepGoZmNR6AcbrpJ4"
access_token_secret="TDbgAuKjfA2hjnq4I0cWWI16nNqq44vQOGHt10DUZhjpt"
cluster_name="maprdemo"

def html_decode(s):
    htmlCodes = [("'", '&#39;'),('"', '&quot;'),('>', '&gt;'),('<', '&lt;'),('&', '&amp;')]
    for code in htmlCodes:
        s = s.replace(code[0], code[1])
    return s

def format_html_row(jsonin):
#    jsonin = unicode(jsonin)
    tweet = str(jsonin["tweet"]).encode('utf-8')
    return "[\'{}\',\'<img src=\"{}\"/>\',\'{}\',\'{}\']".format(jsonin["timestamp"], jsonin["image_url"], jsonin["username"],tweet)


    def on_error(self, status):
        print status


def create_report(data):
    template = open("html_template.txt", "r").read()
    new = template.replace("##data##", data)
    output = open("tweet_report.html", "w")
    output.writelines(new)




class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):

        j = json.loads(data)
        print "*" * 20

        #result reports
        timestamp = datetime.fromtimestamp(time.time())
        str_timestamp = str(timestamp.strftime("%m_%d_%Y-%H_%M_%S"))
        user_name = j["user"]["screen_name"]
        # of = open("../data/" + user_name + str_timestamp + ".json", "w")
        # out_file = "/mapr/" + cluster_name + "/user/mapr/data3/output.json"
        # off = open(out_file, "a")
        #
        es = {}
        es["id"] = str(j["id"]).replace("'","").replace("\"", "")
        es["username"] = user_name
        es["tweet"] = j["text"]
        es["timestamp"] = str(datetime.fromtimestamp(time.time()).isoformat())
        es["image_url"] = j["user"]["profile_image_url"]
        es_j = json.dumps(es)

        #print format_html_row(es)

        #
        # of.write(unicode(data)) #write individual file
        # off.writelines(unicode(data)) #append to big file
        #
        # #submit to elasticsearch
        # es_api = elasticsearch.Elasticsearch()
        # es_api.index(
        #     index="tweets",
        #     doc_type="boeing",
        #     id=es["id"],
        #     body=es
        #     )

        #print output to console
        pprint.pprint(es)
        create_report(es.values().__str__())
        #print "[\'{}\',\'<img src=\"{}\"/>\',\'{}\',\'{}\']".format(es["timestamp"], es["image_url"], es["username"],es["tweet"])

        print "*" * 20

        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['nfl', '49ers', 'cardinals', 'rams', 'seahawks'])




