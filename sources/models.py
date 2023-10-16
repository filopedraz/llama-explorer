from django.db import models


class GithubUser(models.Model):
    gh_id = models.CharField(max_length=100)
    login = models.CharField(max_length=100)

    url = models.URLField(max_length=200, null=True, blank=True)
    avatar_url = models.URLField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    twitter_username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return self.login


class Repository(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    stars = models.IntegerField()
    forks = models.IntegerField()
    watchers = models.IntegerField()
    open_issues_count = models.IntegerField()
    language = models.CharField(max_length=100)
    license = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    topics = models.TextField()

    def __str__(self) -> str:
        return self.name


class Commit(models.Model):
    sha = models.CharField(max_length=100, primary_key=True)
    message = models.TextField()
    developer = models.ForeignKey(
        GithubUser, on_delete=models.CASCADE, related_name="commits", null=True
    )
    repository = models.ForeignKey(
        Repository, on_delete=models.CASCADE, related_name="commits"
    )
    created_at = models.DateTimeField()
