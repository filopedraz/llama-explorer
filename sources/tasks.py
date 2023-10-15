from celery import shared_task

from sources import models, services


@shared_task(bind=True, name="fetch_and_save_repository_task")
def fetch_and_save_repository_task(self, repo):
    services.fetch_and_save_repository(repo)


@shared_task(bind=True, name="fetch_and_save_all_repositories_task")
def fetch_and_save_all_repositories_task(self):
    for repo in services.load_repositories():
        fetch_and_save_repository_task.delay(repo)


@shared_task(bind=True, name="fetch_and_save_commits_task")
def fetch_and_save_commits_task(self, repo):
    services.fetch_and_save_commits(repo)


@shared_task(bind=True, name="fetch_and_save_all_commits_task")
def fetch_and_save_all_commits_task(self):
    for repo in services.load_repositories():
        fetch_and_save_commits_task.delay(repo)


@shared_task(bind=True, name="fetch_and_save_contributor_task")
def fetch_and_save_contributor_task(self, username):
    services.fetch_and_save_contributor(username)


@shared_task(bind=True, name="fetch_and_save_all_contributors_task")
def fetch_and_save_all_contributors_task(self):
    for developer in models.GithubUser.objects.all():
        fetch_and_save_contributor_task.delay(developer.login)


@shared_task(bind=True, name="fetch_and_save_developer_coordinates_task")
def fetch_and_save_developer_coordinates_task(self, username):
    services.fetch_and_save_developer_coordinates(username)


@shared_task(bind=True, name="fetch_and_save_all_developers_coordinates_task")
def fetch_and_save_all_developers_coordinates_task(self):
    for developer in models.GithubUser.objects.all():
        fetch_and_save_developer_coordinates_task.delay(developer.login)
