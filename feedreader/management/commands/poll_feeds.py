"""
This command polls all of the Feeds and removes old entries.
"""
from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Feed, Entry
from ...utils import poll_feed

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Polls all Feeds for Entries."

    def add_arguments(self, parser):
        parser.add_argument(
            "--verbose",
            action="store_true",
            dest="verbose",
            default=False,
            help="Print progress on command line",
        )

    def handle(self, *args, **options):
        verbose = options["verbose"]
        feeds = Feed.objects.all()
        num_feeds = len(feeds)
        num_new_entries = 0

        if verbose:
            print(f"{num_feeds} feeds to process")

        for count, feed in enumerate(feeds, 1):
            if verbose:
                print(f"({count}/{num_feeds}) Processing Feed {feed.title}")

            num_new_entries += poll_feed(feed, verbose)

            # Remove older entries
            entries = Entry.objects.filter(feed=feed)[settings.MAX_ENTRIES_SAVED :]

            for entry in entries:
                entry.delete()

            if verbose:
                print(f"Deleted {len(entries)} entries from feed {feed.title}")

        logger.info(f"Feedreader poll_feeds completed successfully, {num_new_entries} new entries found")
