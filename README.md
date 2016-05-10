# PoliticalTweets

## Dependencies

### Python

The collection and update scripts require [Python 2.7.11][1] or
higher

Additionally, the scripts require the installation of a couple of Python packages:

[Tweepy][2]:

	pip install tweepy

[Py2neo][3]:

	pip install py2neo

[Scrapy][4]:

	pip install scrapy

### Neo4j

[Neo4j][5] can be installed in any Windows or Unix environment

For the purposes of this project we will be using our own Neo4j instance which is located at <http://battlestar.lkdyn.net:7474/browser/>

## Setup

Our inital import script requires valid Twitter API keys from [https://apps.twitter.com][6]

After setting up a new application and obtaining valid keys, replace lines 9-12 in *import\_political\_tweets.py*:

    CONSUMER_KEY = 'CONSUMER_KEY'
    CONSUMER_SECRET = 'CONSUMER_SECRET'
    ACCESS_TOKEN_KEY = 'ACCESS_TOKEN'
    ACCESS_TOKEN_SECRET = 'ACCESS_TOKEN_SECRET'
    
If you are using your own instance of Neo4j, update the URL in the following places:

* Line 27 of *import\_political\_tweets.py*
* Line 9 of *twitterscrapy/spiders/tweety.py*
* Line 13 of *twitterscrapy/pipelines.py*

## Usage

### Import and Update scripts

In order to collect the initial dataset run

	python import_political_tweets.py
	
This script takes a while to run depending on how many tweets you wish to collect. Quit it once you reach your desired amount. All Tweets are imported into the Neo4j database and also recorded in the *dataset.json* file.

In order to update retweet and favorite counts, we used a Twitter scraper.

Run it using the following command in the working directory:

	scrapy crawl tweety


### Neo4j queries and cyphers

Sentiment Analysis Queries were used from <https://github.com/kvangundy/basic-sentiment-analyzer>

In order to use Neo4j to run sentiment analysis:

* Import the *sentimentdict.csv* into your local Neo4j import directory
	
	This was located at */usr/share/neo4j/import* in our linux installation
  
* Run the *importDictionary.cypher* by querying it line by line
* Run the *sentimentAnalysisScript.cypher* line by line except the first two files, and replace {word} with text

Additional queries for extracting data for analysis can be found in the *Neo4j Queries.cql* file

[1]:	https://www.python.org/downloads/release/python-2711/
[2]:	https://github.com/tweepy/tweepy
[3]:	http://py2neo.org/v3/
[4]:	http://scrapy.org
[5]:	http://neo4j.com/download/
[6]:	https://apps.twitter.com