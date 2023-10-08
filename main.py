import os
import time
import requests
import logging
import pandas as pd

from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv()

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Data Structure
# General Info (login, avatar_url, name, type, blog, location, email, 
# hireable, bio, twitter_username, public_repos, public_gists, followers, 
# following, created_at, updated_at, html_url etc) | Repositories Starred (list of the repositories in our list).

@retry(stop=stop_after_attempt(3), wait=wait_fixed(60*30))
def fetch_user_info(username):
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        raise ValueError("GitHub token is not set in .env file")

    url = f"https://api.github.com/users/{username}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Mozilla/5.0",
        "Authorization": f"token {token}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        raise ValueError("Rate limit exceeded")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(60*30))
def fetch_stars_page(repository, page):
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise ValueError("GitHub token is not set in .env file")

    url = f"https://api.github.com/repos/{repository}/stargazers"
    headers = { 
        "Accept": "application/vnd.github.v3+json", 
        "User-Agent": "Mozilla/5.0", 
        "Authorization": f"token {token}"
    }
    response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
    if response.status_code == 200:
        logging.info(f"Fetched page {page} for {repository} with {len(response.json())} stargazers")
        return None if len(response.json()) == 0 else response
    elif response.status_code == 403:
        raise ValueError("Rate limit exceeded")
    

def fetch_stargazers(repository):
    stargazers = []
    page = 1

    while True:
        response = fetch_stars_page(repository, page)

        if response is None:
            break
        
        stargazers.extend([user['login'] for user in response.json()])

        page += 1

    logging.info(f"Found {len(stargazers)} stargazers for {repository}")
    return stargazers

def load_repositories(filename="repositories.txt"):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]
    
def user_record_exists(df, username, repo):
    if df.empty:
        return False
    return df[(df["login"] == username) & (df["repository"] == repo)].any().any()


if __name__ == "__main__":
    repositories = load_repositories()
    logging.info("Loaded repositories")

    df = pd.read_csv("./data/data.csv") if os.path.exists("./data/data.csv") else pd.DataFrame()
    logging.info(f"Loaded df with {len(df)} records")

    while True:
        for repo in repositories:
            try:
                logging.info(f"Repository to process {repo}")
                users = fetch_stargazers(repo)
                for user in users:
                    if not user_record_exists(df, user, repo):
                        try:
                            user_info = fetch_user_info(user)
                            user_info["repository"] = repo
                            df = pd.concat([df, pd.DataFrame([user_info])], ignore_index=True)
                            df.to_csv("./data/data.csv", index=False)
                        except Exception as e:
                            logging.error(f"Failed to process {user} with error {e}")
                logging.info(f"Processed {repo}")
            except Exception as e:
                logging.error(e)