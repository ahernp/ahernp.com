from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import Log

import logging

logger = logging.getLogger(__name__)

DAYS_TO_KEEP = 30


class Command(BaseCommand):
    help = "Deletes older Log entries."

    def add_arguments(self, parser):
        parser.add_argument("keep_delta", nargs="?", default=DAYS_TO_KEEP, type=int)
        parser.add_argument(
            "--verbose",
            action="store_true",
            dest="verbose",
            default=False,
            help="Print progress on command line",
        )

    def handle(self, *args, **options):
        verbose = options["verbose"]

        keep_delta = options["keep_delta"]

        delete_before = timezone.now() - timedelta(days=keep_delta)

        if verbose:
            log_count = Log.objects.filter(datetime__lt=delete_before).count()
            print(f"{log_count} Log entries to delete (older than {delete_before})")

        Log.objects.filter(datetime__lt=delete_before).delete()

        logger.info("Log entries deleted successfully")
