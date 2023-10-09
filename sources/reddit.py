import os
import time
import requests
import logging
import pandas as pd

from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def login():
    response = requests.post("https://www.reddit.com/api/v1/access_token",
                             headers={"User-Agent": "Mozilla/5.0", },
                             data={
                                 "grant_type": "password",
                                 "username": os.getenv("REDDIT_USERNAME"),
                                 "password": os.getenv("REDDIT_PASSWORD"),
                             }, auth=(os.getenv("REDDIT_CLIENT_ID"), os.getenv("REDDIT_CLIENT_SECRET")))
    return response.json().get("access_token")


def fetch_comments(post_id, parent_id=None):
    url = f"https://oauth.reddit.com/r/LocalLLaMA/comments/{post_id}"
    response = requests.get(url, headers={
        "Authorization": f"bearer {login()}",
        "User-Agent": "Mozilla/5.0"
    })
    comments_data = response.json()

    comments = []
    for comment in comments_data[1]["data"]["children"]:
        comment_body = comment["data"]["body"]
        comments.append(comment_body)
    return comments


def post_record_exists(df, post_id):
    return len(df[df["id"] == post_id]) == 0


if __name__ == "__main__":
    df = pd.read_csv(
        "./data/reddit.csv") if os.path.exists("./data/reddit.csv") else pd.DataFrame()
    logging.info(f"Loaded df with {len(df)} records")

    end_time = time.time()
    start_time = (datetime.utcnow() - timedelta(days=365)).timestamp()

    for subreddit in ["LocalLLaMA"]:

        base_url = f"https://oauth.reddit.com/r/{subreddit}/new"
        after = None

        while True:
            params = {
                "before": end_time,
                "limit": 100
            }
            if after:
                params["after"] = after

            response = requests.get(base_url, headers={
                "Authorization": f"bearer {login()}",
                "User-Agent": "Mozilla/5.0"
            }, params=params)

            data = response.json().get("data", {})
            posts = data.get("children", [])

            if not posts:
                break

            for post in posts:
                if not post_record_exists(df, post["data"]["id"]):
                    post_data = post["data"]
                    created_utc = post_data["created_utc"]

                    if created_utc < start_time:
                        break

                    comments = fetch_comments(post_data["id"])
                    comments = "\n===\n".join(comments)
                    post_info = {
                        "id": post_data["id"],
                        "title": str(post_data["title"]),
                        "created_utc": post_data["created_utc"],
                        "author": str(post_data["author"]),
                        "comments": str(comments),
                        "selftext_html": str(post_data["selftext_html"]),
                        "url": post_data["url"],
                        "selftext": str(post_data["selftext"]),
                        "num_comments": post_data["num_comments"],
                        "likes": post_data["likes"],
                        "score": post_data["score"],
                        "subreddit": subreddit
                    }
                    df = pd.concat([df, pd.DataFrame([post_info])],
                                   ignore_index=True)
                    df.to_csv("./data/reddit.csv", index=False)

            logging.info(f"Saved {len(posts)} posts")

            after = data.get("after")
            if not after:
                break

            time.sleep(1)
