import logging

from django.utils.dateparse import parse_datetime
from geopy.geocoders import Nominatim

from sources import models
from sources.clients import github

logger = logging.getLogger(__name__)


def get_geolocator():
    geolocator = Nominatim(user_agent="Llama Explorer")
    return geolocator


def load_repositories(filename="./repositories.txt"):
    with open(filename) as f:
        return [line.strip() for line in f.readlines() if line.strip() != ""]


def fetch_and_save_repository(repo):
    repo_info = github.fetch_repository(repo)
    if repo_info is not None:
        created_at = parse_datetime(repo_info.get("created_at"))
        updated_at = parse_datetime(repo_info.get("updated_at"))

        license_info = repo_info.get("license")
        license_name = license_info.get("name") if license_info else None

        models.Repository.objects.update_or_create(
            name=repo,
            defaults={
                "stars": repo_info.get("stargazers_count", 0),
                "forks": repo_info.get("forks", 0),
                "watchers": repo_info.get("watchers", 0),
                "open_issues_count": repo_info.get("open_issues_count", 0),
                "language": repo_info.get("language", ""),
                "license": license_name,
                "created_at": created_at,
                "updated_at": updated_at,
                "description": repo_info.get("description", ""),
                "topics": ", ".join(repo_info.get("topics", [])),
            },
        )
        logger.info(f"Repository {repo} updated/created successfully")
    else:
        logger.error(f"Repository {repo} failed to process.")


def fetch_and_save_commits(repo):
    commits_info = github.fetch_commits_info(repo, "2022-11-30T00:00:00Z")

    for commit_info in commits_info:
        author_info = commit_info.get("author")
        author = author_info.get("login") if author_info else None
        avatar_url = author_info.get("avatar_url") if author_info else None

        commit = commit_info.get("commit")
        commit_date = parse_datetime(commit.get("author").get("date"))

        if author is not None:
            if models.GithubUser.objects.filter(login=author).count() == 0:
                developer = models.GithubUser.objects.create(
                    login=author, avatar_url=avatar_url
                )
            else:
                developer = models.GithubUser.objects.get(login=author)

            models.Commit.objects.update_or_create(
                sha=commit_info.get("sha"),
                defaults={
                    "repository": models.Repository.objects.get(name=repo),
                    "developer": developer,
                    "created_at": commit_date,
                    "message": commit.get("message"),
                },
            )
    logger.info(
        f"{len(commits_info)} commits for repository {repo} updated/created successfully"
    )


def fetch_and_save_contributor(username):
    user_info = github.fetch_user_info(username)
    if user_info is not None:
        models.GithubUser.objects.update_or_create(
            login=user_info.get("login"),
            defaults={
                "gh_id": user_info.get("id"),
                "url": user_info.get("url"),
                "avatar_url": user_info.get("avatar_url"),
                "name": user_info.get("name"),
                "location": user_info.get("location"),
                "company": user_info.get("company"),
                "bio": user_info.get("bio"),
                "twitter_username": user_info.get("twitter_username"),
                "email": user_info.get("email"),
            },
        )
        logger.info(f"User {username} updated/created successfully")
    else:
        logger.error(f"User {username} failed to process.")


def fetch_and_save_developer_coordinates(username):
    geolocator = get_geolocator()
    developer = models.GithubUser.objects.get(login=username)
    if developer.latitude is None:
        location = geolocator.geocode(developer.location)
        if location is not None:
            developer.latitude = location.latitude
            developer.longitude = location.longitude
            developer.save()
            logger.info(f"Coordinates for {username} updated/created successfully")
        else:
            logger.error(f"Coordinates for {username} failed to process.")
    else:
        logger.info(f"Coordinates for {username} already exist")
