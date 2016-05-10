# -*- coding: utf-8 -*-
import scrapy
import locale
from py2neo import neo4j

class TweetySpider(scrapy.Spider):
    name = "tweety"
    allowed_domains = ["twitter.com"]
    url = "http://battlestar.lkdyn.net:7474/db/data/"
    graph = neo4j.Graph(url)

    def start_requests(self):
        results = self.graph.cypher.execute("MATCH (u:User)-[:POSTS]->(t:Tweet) RETURN u.screen_name, t.id, "
                                            "t.favorites ORDER BY t.favorites, t.retweets LIMIT 8000")
        for row in results:
            screen_name = str(row['u.screen_name'])
            status = str(row['t.id'])
            yield scrapy.Request('https://twitter.com/' + screen_name + '/status/' + status, self.parse,
                             meta={ 'screen_name': screen_name, 'status': status})

    def parse(self, response):
        tweet = response.css('.js-original-tweet')[0]
        retweets = tweet.css('.js-stat-retweets > a > strong::text').extract_first()
        favorites = tweet.css('.js-stat-favorites > a > strong::text').extract_first()


        if retweets is not None:
            retweets = str(retweets).replace(',', '')
            retweets = locale.atoi(retweets)
        else:
            retweets = 0

        if favorites is not None:
            favorites = favorites.replace(',', '')
            favorites = locale.atoi(favorites)
        else:
            favorites = 0

        yield {
            'screen_name': response.meta['screen_name'],
            'status': response.meta['status'],
            'retweets': retweets,
            'favorites': favorites
        }
