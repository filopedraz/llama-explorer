import logging
from datetime import datetime, timedelta

import tweepy

from backend import settings


def initialize_api():
    auth = tweepy.OAuthHandler(
        settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY
    )
    auth.set_access_token(
        settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def fetch_tweets(user=None, query=None):
    api = initialize_api()

    tweets_list = []
    end_date = datetime.utcnow() - timedelta(days=365)

    if user:
        for status in tweepy.Cursor(
            api.user_timeline, screen_name=user, tweet_mode="extended"
        ).items():
            if status.created_at < end_date:
                break
            tweets_list.append(status._json)
    elif query:
        for status in tweepy.Cursor(
            api.search, q=query, lang="en", tweet_mode="extended"
        ).items():
            if status.created_at < end_date:
                break
            tweets_list.append(status._json)

    return tweets_list


if __name__ == "__main__":
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

        logging.info(f"Saved {len(tweets)} tweets")
