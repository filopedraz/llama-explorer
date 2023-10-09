import os
import logging
import pandas as pd
import tweepy

from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Twitter Metrics
# 0. List of all the tweets of yesterday with title and some stats (likes, retweets, replies, etc).
# 1. Generic Yesterday summary of content
# 2. Most mentioned tools, languages, frameworks, etc.


def initialize_api():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    return api


def fetch_tweets(user=None, query=None):
    api = initialize_api()

    tweets_list = []
    end_date = datetime.utcnow() - timedelta(days=365)

    if user:
        for status in tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode="extended").items():
            if status.created_at < end_date:
                break
            tweets_list.append(status._json)
    elif query:
        for status in tweepy.Cursor(api.search, q=query, lang="en", tweet_mode="extended").items():
            if status.created_at < end_date:
                break
            tweets_list.append(status._json)

    return tweets_list


if __name__ == "__main__":
    df_path = "./data/twitter.csv"
    df = pd.read_csv(df_path) if os.path.exists(df_path) else pd.DataFrame()
    logging.info(f"Loaded df with {len(df)} records")

    for user in ["jack"]:
        tweets = fetch_tweets(user=user)

        for tweet in tweets:
            tweet_info = {
                "id": tweet["id"],
                "text": tweet["full_text"],
                "created_at": tweet["created_at"],
                "likes": tweet["favorite_count"],
                "retweets": tweet["retweet_count"],
                "user_name": tweet["user"]["screen_name"],
            }
            df = pd.concat([df, pd.DataFrame([tweet_info])], ignore_index=True)
            df.to_csv(df_path, index=False)

        logging.info(f"Saved {len(tweets)} tweets")
