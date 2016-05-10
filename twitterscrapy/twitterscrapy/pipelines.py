# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from py2neo import neo4j
from py2neo import Node

class TwitterscrapyPipeline(object):

    def __init__(self):
        self.url = "http://battlestar.lkdyn.net:7474/db/data/"
        self.graph = neo4j.Graph(self.url)

    def process_item(self, item, spider):
        # user = self.graph.get_or_create(neo4j.Node, 'User', 'screen_name', 'RightmindsRus')
        self.graph.cypher.execute("MATCH (n:Tweet {id:" + item['status'] + "}) SET n.favorites = " + str(item[
            'favorites']) + ", n.retweets = " + str(item['retweets']))

        print item
        return item
