import logging

from django.core.management.base import BaseCommand

from sources import services

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Script to fetch all the commits"

    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        for repo in services.load_repositories():
            services.fetch_and_save_commits(repo)
