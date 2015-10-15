import twitter
import json
import io
from datetime import datetime, timedelta
import time


def oauth_login():

    CONSUMER_KEY = 'h9ZHlkz53jYPWFoxSZNoFtuf9'
    CONSUMER_SECRET = 'I4DEEOiNbR1OTO0UM5j5OsyLv7mcFAOySu6U4OHuVg85T0CpFm'
    OAUTH_TOKEN = '23088031-k7lxpDWd9o5lcqrnkjZfbNsVNepGoZmNR6AcbrpJ4'
    OAUTH_TOKEN_SECRET = 'TDbgAuKjfA2hjnq4I0cWWI16nNqq44vQOGHt10DUZhjpt'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

def twitter_search(twitter_api, q, max_results=1000, **kw):
    output_text = ""
    output_json = ""

    search_results = twitter_api.search.tweets(q=q, count=100, **kw)

    output_file = open("./data/" + q + ".txt", "w")
    output_file_json = open("./data/" + q + ".json", "w")

    statuses = search_results['statuses']

    max_results = min(1000, max_results)
    tweet_count = 0

    for _ in range(10):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e:
            break

        kwargs = dict([ kv.split('=')
                        for kv in next_results[1:].split("&") ])

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

        tweet_count += 100
        # print tweet_count

        if len(statuses) > max_results:
            break

        for r in statuses:
            username = r["user"]["screen_name"]
            friend_count = str(r["user"]["friends_count"])

            try:
                tweet_text = str(r["text"]).encode('utf-8', errors="replace")
                tweet_text = tweet_text.replace("\n", "")
            except:
                tweet_text = ""

            substr_t =  username + "|" + friend_count + "|" + tweet_text + "\n"


            if tweet_text != "":
                output_text += json.dumps(r) + "\n"

                #result reports
                timestamp = datetime.fromtimestamp(time.time())
                str_timestamp = str(timestamp.strftime("%m_%d_%Y-%H_%M_%S"))
                user_name = r["user"]["screen_name"]
                of = open("/temp/gallo/" + user_name + str_timestamp + ".json", "w")
                of.write(json.dumps(r)) #write individual file

            #json output



    print "Writing: ", output_file.name
    output_file.write(output_text) #bigfile

twitter_api = oauth_login()
#print "Authed to Twitter. Searching now..."

#searches = ['apothic', 'boones farm', 'barefoot cellars', 'columbia winery', 'covey run', 'carlorossi']
searches = ['Boones Farm', 'Apothic', 'CarloRossi', 'Carlo Rossi']

for q in searches:
    #q = "apothic"
    results = twitter_search(twitter_api, q, max_results=1000)
