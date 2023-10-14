import logging

import requests
from tenacity import retry, stop_after_attempt, wait_fixed

from backend import settings

logger = logging.getLogger(__name__)

GH_BASE_URL = "https://api.github.com"


def get_headers():
    return {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Mozilla/5.0",
        "Authorization": f"token {settings.GITHUB_TOKEN}",
    }


def handle_response(response):
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        raise ValueError("Rate limit exceeded")


@retry(stop=stop_after_attempt(3), wait=wait_fixed(60 * 30))
def fetch_user_info(username):
    url = f"{GH_BASE_URL}/users/{username}"
    response = requests.get(url, headers=get_headers())
    return handle_response(response)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(60 * 30))
def fetch_stars_page(repository, page):
    url = f"{GH_BASE_URL}/repos/{repository}/stargazers"
    response = requests.get(
        url, headers=get_headers(), params={"page": page, "per_page": 100}
    )
    return handle_response(response)


def fetch_repository_stars(repository):
    stargazers = []
    page = 1
    while True:
        response = fetch_stars_page(repository, page)
        if response is None:
            break
        stargazers.extend([user["login"] for user in response.json()])
        page += 1
    return stargazers


def fetch_repository_contributors(repository):
    raise NotImplementedError


def fetch_repository_info(repository):
    url = f"{GH_BASE_URL}/repos/{repository}"
    response = requests.get(url, headers=get_headers())
    return handle_response(response)
