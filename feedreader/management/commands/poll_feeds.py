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

        if verbose:
            print("%d feeds to process" % (num_feeds))

        for count, feed in enumerate(feeds, 1):
            if verbose:
                print(
                    "({count}/{num_feeds}) Processing Feed {title}".format(
                        count=count, num_feeds=num_feeds, title=feed.title
                    )
                )

            poll_feed(feed, verbose)

            # Remove older entries
            entries = Entry.objects.filter(feed=feed)[settings.MAX_ENTRIES_SAVED :]

            for entry in entries:
                entry.delete()

            if verbose:
                print("Deleted %d entries from feed %s" % ((len(entries), feed.title)))

        logger.info("Feedreader poll_feeds completed successfully")
