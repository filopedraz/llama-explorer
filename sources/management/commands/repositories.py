import logging

from django.core.management.base import BaseCommand

from sources.services import fetch_and_save_repositories_info

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Script to load all the currencies"

    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        fetch_and_save_repositories_info()
