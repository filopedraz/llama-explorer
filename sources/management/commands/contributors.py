import logging

from django.core.management.base import BaseCommand

from sources import models, services

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Script to fetch all the contributors"

    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        for developer in models.GithubUser.objects.all():
            services.fetch_and_save_contributor(developer.login)
