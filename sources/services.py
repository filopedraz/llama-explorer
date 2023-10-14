import logging

from django.utils.dateparse import parse_datetime

from sources import models
from sources.clients import github

logger = logging.getLogger(__name__)


def load_repositories(filename="./repositories.txt"):
    with open(filename) as f:
        return [line.strip() for line in f.readlines() if line.strip() != ""]


def fetch_and_save_repositories_info():
    for repo in load_repositories():
        try:
            repo_info = github.fetch_repository_info(repo)

            created_at = parse_datetime(repo_info.get("created_at"))
            updated_at = parse_datetime(repo_info.get("updated_at"))

            license_info = repo_info.get("license")
            license_name = license_info.get("name") if license_info else None

            models.Repository.objects.update_or_create(
                name=repo_info.get("name"),
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
        except Exception as e:
            logger.error(e)
