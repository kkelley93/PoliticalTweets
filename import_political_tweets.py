import tweepy
import pprint
import json
import time
from py2neo import neo4j

import json

CONSUMER_KEY = 'CONSUMER_KEY'
CONSUMER_SECRET = 'CONSUMER_SECRET'
ACCESS_TOKEN_KEY = 'ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'ACCESS_TOKEN_SECRET'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)



pp = pprint.PrettyPrinter(indent=4)


class MyStreamListener(tweepy.StreamListener):

    first_run = True
    url = "http://battlestar.lkdyn.net:7474/db/data/"
    twts = []
    results = 0
    md = ['maryland', 'Maryland', 'md', 'MD']
    query = """
        UNWIND {tweets} AS t

        WITH t
        ORDER BY t.id

        WITH t,
             t.entities AS e,
             t.user AS u,
             t.retweeted_status AS retweet

        MERGE (tweet:Tweet {id:t.id})
        SET tweet.text = t.text,
            tweet.created_at = t.created_at,
            tweet.favorites = t.favorite_count

        MERGE (user:User {screen_name:u.screen_name})
        SET user.name = u.name,
            user.location = u.location,
            user.followers = u.followers_count,
            user.following = u.friends_count,
            user.statuses = u.statusus_count,
            user.profile_image_url = u.profile_image_url

        MERGE (user)-[:POSTS]->(tweet)

        MERGE (source:Source {name:t.source})
        MERGE (tweet)-[:USING]->(source)

        FOREACH (h IN e.hashtags |
          MERGE (tag:Hashtag {name:LOWER(h.text)})
          MERGE (tag)-[:TAGS]->(tweet)
        )

        FOREACH (u IN e.urls |
          MERGE (url:Link {url:u.expanded_url})
          MERGE (tweet)-[:CONTAINS]->(url)
        )

        FOREACH (m IN e.user_mentions |
          MERGE (mentioned:User {screen_name:m.screen_name})
          ON CREATE SET mentioned.name = m.name
          MERGE (tweet)-[:MENTIONS]->(mentioned)
        )

        FOREACH (r IN [r IN [t.in_reply_to_status_id] WHERE r IS NOT NULL] |
          MERGE (reply_tweet:Tweet {id:r})
          MERGE (tweet)-[:REPLY_TO]->(reply_tweet)
        )

        FOREACH (retweet_id IN [x IN [retweet.id] WHERE x IS NOT NULL] |
            MERGE (retweet_tweet:Tweet {id:retweet_id})
            MERGE (tweet)-[:RETWEETS]->(retweet_tweet)
        )
        """



    def on_status(self, status):
        # print status.user.location
        if self.first_run:
            self.first_run = False
            self.graph = neo4j.Graph(self.url)

        if status.user.location:
            if any(x in status.user.location for x in self.md):
                # print status._json
                self.results = self.results + 1
                print "Current Results: " + str(self.results)
                self.twts.append(status._json)
        if len(self.twts) == 10:
            print "Importing tweets..."
            with open("dataset.json", "a") as myfile:
                json.dump(self.twts, myfile)
            self.graph.cypher.execute(self.query, tweets=self.twts)
            self.twts = []

    def on_error(self, status_code):
        print "errored"
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['bernie', 'sanders', 'donald', 'trump', 'hillary', 'clinton', 'marco', 'rubio',
                       'ted', 'cruz', 'president', 'primaries', 'DNC', 'republican', 'Conservative', 'Donald Trump',
                       'politics', 'political', 'democrat', 'liberal', 'HRC', 'DNC', 'potus', 'hillaryclinton',
                       'donaldtrump', 'berniesanders', 'tedcruz', 'marcorubio', 'cruzcrew', 'trumptrain',
                       'trump2016', 'makeamericagreatagain', 'stillsanders', 'imwithher'
                       'feelthebern', 'economy', 'health care',  'foreign policy', 'education', 'immigration',
                       'abortion', 'same sex marriage', 'gun control', 'vote', 'election', 'debate', 'potus2016'],
                follow=['1339835893', '216776631', '25073877', '15745368', '23022687'])
