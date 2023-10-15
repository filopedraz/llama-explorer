import logging

import requests

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


def fetch_user_info(username):
    url = f"{GH_BASE_URL}/users/{username}"
    response = requests.get(url, headers=get_headers())
    return handle_response(response)


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


def fetch_repository(repository):
    url = f"{GH_BASE_URL}/repos/{repository}"
    try:
        response = requests.get(url, headers=get_headers())
        return handle_response(response)
    except Exception as error:
        logger.error(error)
        return None


def fetch_commits_info(repository, since_date=None):
    url = f"{GH_BASE_URL}/repos/{repository}/commits"
    all_commits = []
    page = 1

    while True:
        params = {"since": since_date, "per_page": 100, "page": page}
        response = requests.get(url, headers=get_headers(), params=params)

        commits = handle_response(response)
        if not commits:
            break

        all_commits.extend(commits)
        page += 1

    return all_commits
