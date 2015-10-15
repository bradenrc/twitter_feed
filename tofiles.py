#!/usr/bin/python

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time
from datetime import datetime, timedelta
import os
import pprint

consumer_key="h9ZHlkz53jYPWFoxSZNoFtuf9"
consumer_secret="I4DEEOiNbR1OTO0UM5j5OsyLv7mcFAOySu6U4OHuVg85T0CpFm"
access_token="23088031-k7lxpDWd9o5lcqrnkjZfbNsVNepGoZmNR6AcbrpJ4"
access_token_secret="TDbgAuKjfA2hjnq4I0cWWI16nNqq44vQOGHt10DUZhjpt"

g_file = open("gallo.txt", "r")

g_list = []

for row in g_file:
    g_list.append(row.replace("\n", "").encode('utf-8', errors="ignore"))



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
        of = open("/temp/gallo_twitter_data/" + user_name + str_timestamp + ".json", "w")
        of.write(unicode(data)) #write individual file

        #print output to console
        pprint.pprint(data)
        print "*" * 20

        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['apothic', 'boonesfarm', 'barefootcellars', 'columbiawinery', 'coveyrun'])
#    stream.filter(track=g_list)



