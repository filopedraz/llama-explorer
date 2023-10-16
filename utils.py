from datetime import datetime

import pandas as pd
from django.db.models import Count, Q

from sources import models


def fetch_basic_metrics():
    rt = models.Repository.objects.all().count()
    mupl = (
        models.Repository.objects.values("language")
        .annotate(count=Count("language"))
        .order_by("-count")[0]
    )
    cwmc = (
        models.GithubUser.objects.values("location")
        .annotate(count=Count("location"))
        .order_by("-count")[0]
    )
    return (
        rt,
        f"{mupl['language']} ({mupl['count']})",
        f"{cwmc['location']} ({cwmc['count']})",
    )


def fetch_best_contributor_of_the_day():
    now = datetime.now()

    bcotd = (
        models.GithubUser.objects.annotate(
            count=Count("commits", filter=Q(commits__created_at__date=now.date()))
        )
        .values("login", "count", "avatar_url")
        .order_by("-count")
        .first()
    )
    return bcotd["login"], bcotd["count"], bcotd["avatar_url"]


def fetch_most_starred_repositories():
    most_starred_repositories = models.Repository.objects.order_by("-stars")[:100]
    df_most_starred_repositories = pd.DataFrame(
        most_starred_repositories.values(
            "name",
            "stars",
            "forks",
            "watchers",
            "open_issues_count",
            "language",
            "license",
            "created_at",
            "updated_at",
        )
    )
    df_most_starred_repositories.columns = [
        "Name",
        "Stars",
        "Forks",
        "Watchers",
        "Open Issues",
        "Language",
        "License",
        "Created",
        "Updated",
    ]
    df_most_starred_repositories.fillna("Not Available", inplace=True)
    return df_most_starred_repositories


def fetch_most_active_contributors():
    df_most_active_contributors = pd.DataFrame(
        models.GithubUser.objects.values(
            "login", "location", "company", "twitter_username", "email", "name"
        )
        .annotate(count=Count("commits"))
        .order_by("-count")[:100]
    )
    df_most_active_contributors.columns = [
        "Username",
        "Location",
        "Company",
        "Twitter",
        "Email",
        "Name",
        "Commits",
    ]
    df_most_active_contributors.fillna("Not Available", inplace=True)
    return df_most_active_contributors


def fetch_contributors_locations():
    contributors = models.GithubUser.objects.filter(
        latitude__isnull=False, longitude__isnull=False
    )
    df_contributors_locations = pd.DataFrame.from_records(
        contributors.values("login", "latitude", "longitude")
    )
    df_contributors_locations.columns = ["username", "lat", "lon"]
    return df_contributors_locations


def fetch_most_used_programming_languages():
    languages_qs = (
        models.Repository.objects.values("language")
        .annotate(count=Count("language"))
        .order_by("-count")
    )

    df_languages = pd.DataFrame.from_records(languages_qs)
    df_languages.columns = ["Programming Language", "Count"]
    return df_languages.sort_values('Count', ascending=False)
