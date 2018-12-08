#from twython import Twython
#from twython import TwythonStreamer
import tweepy
import csv
import json
import pandas as pd

#Load in credentials
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

#Key
auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

## To create different queuries for searching tweets look here: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
query = { 'q': '#TheGameAwards',
        'count': 5,
        'lang': 'en',
        'include_entities': 'true',
        'tweet_mode': 'extended',
        }

dict_ = {'user': [], 'date': [], 'full_text': [], 'favorite_count': []}

myFile = open('tweets2.csv', 'w', encoding="utf-8")
with myFile:
    writer = csv.writer(myFile)
    for tweet in tweepy.Cursor(api.search, q="#TheGameAwards", count=100, lang="en", since="2018-12-06", tweet_mode='extended').items():
        print(tweet.created_at, tweet.full_text)
        dict_['user'].append(tweet.user.name)
        dict_['date'].append(tweet.created_at)
        dict_['favorite_count'].append(tweet.favorite_count)
        #text_to_write = None
        #if hasattr(tweet, 'retweeted_status'):
         #   if tweet.retweeted_status is None:
        text_to_write = tweet.full_text.encode('utf-8')
        dict_['full_text'].append(tweet.full_text.encode('utf-8'))        
        
        writer.writerow([tweet.user.name, tweet.created_at, tweet.full_text, tweet.favorite_count])

df = pd.DataFrame(dict_)
df.to_csv('results.csv', index=False, header=True, encoding="utf-8")


#b = b'\xf0\x9f\x99\x8c'
#print(b.decode('utf-8'))