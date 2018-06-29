from datetime import datetime
from time import mktime

import feedparser
import pytz

from django.conf import settings
from django.utils import html
from django.utils import timezone

from .models import Entry

import logging

logger = logging.getLogger(__name__)


def update_feed_on_database(feed_from_database, feed_from_xml, verbose):
    if hasattr(feed_from_xml.feed, "bozo_exception"):
        msg = f'Feedreader poll_feeds found Malformed feed, "{feed_from_database.xml_url}": {feed_from_xml.feed.bozo_exception}'
        logger.error(msg)
        if verbose:
            print(msg)
        return

    if hasattr(feed_from_xml.feed, "published_parsed"):
        if feed_from_xml.feed.published_parsed is None:
            published_time = timezone.now()
        else:
            published_time = datetime.fromtimestamp(
                mktime(feed_from_xml.feed.published_parsed)
            )
        try:
            published_time = pytz.timezone(settings.TIME_ZONE).localize(
                published_time, is_dst=None
            )
        except pytz.exceptions.AmbiguousTimeError:
            pytz_timezone = pytz.timezone(settings.TIME_ZONE)
            published_time = pytz_timezone.localize(published_time, is_dst=False)
        if (
            feed_from_database.published_time
            and feed_from_database.published_time >= published_time
        ):
            return
        feed_from_database.published_time = published_time

    for attr in ["title", "title_detail", "link"]:
        if not hasattr(feed_from_xml.feed, attr):
            msg = f'Feedreader poll_feeds. Feed "{feed_from_database.xml_url}" has no {attr}'
            logger.error(msg)
            if verbose:
                print(msg)
            return

    if feed_from_xml.feed.title_detail.type == "text/plain":
        feed_from_database.title = html.escape(feed_from_xml.feed.title)
    else:
        feed_from_database.title = feed_from_xml.feed.title

    feed_from_database.link = feed_from_xml.feed.link

    if hasattr(feed_from_xml.feed, "description_detail") and hasattr(
        feed_from_xml.feed, "description"
    ):
        if feed_from_xml.feed.description_detail.type == "text/plain":
            feed_from_database.description = html.escape(feed_from_xml.feed.description)
        else:
            feed_from_database.description = feed_from_xml.feed.description
    else:
        feed_from_database.description = ""

    feed_from_database.last_polled_time = timezone.now()
    feed_from_database.save()

    return feed_from_database


def skip_entry(entry_from_xml, verbose):
    for attr in ["title", "title_detail", "link", "description"]:
        if not hasattr(entry_from_xml, attr):
            msg = f'Feedreader poll_feeds. Entry "{entry_from_xml.link}" has no {attr}'
            logger.warning(msg)
            if verbose:
                print(msg)
            return True

    if entry_from_xml.title == "":
        msg = f'Feedreader poll_feeds. Entry "{entry_from_xml.link}" has a blank title'
        if verbose:
            print(msg)
        logger.warning(msg)
        return True


def update_entry_on_database(entry_on_database, entry_from_xml):
    if hasattr(entry_from_xml, "published_parsed"):
        if entry_from_xml.published_parsed is None:
            published_time = timezone.now()
        else:
            published_time = datetime.fromtimestamp(
                mktime(entry_from_xml.published_parsed)
            )

            try:
                published_time = pytz.timezone(settings.TIME_ZONE).localize(
                    published_time, is_dst=None
                )
            except pytz.exceptions.AmbiguousTimeError:
                pytz_timezone = pytz.timezone(settings.TIME_ZONE)
                published_time = pytz_timezone.localize(published_time, is_dst=False)

            now = timezone.now()

            if published_time > now:
                published_time = now

        entry_on_database.published_time = published_time

    if entry_from_xml.title_detail.type == "text/plain":
        entry_on_database.title = html.escape(entry_from_xml.title)
    else:
        entry_on_database.title = entry_from_xml.title

    # Lots of entries lack description_detail attributes.
    # Escape their content by default
    if (
        hasattr(entry_from_xml, "description_detail")
        and entry_from_xml.description_detail.type != "text/plain"
    ):
        entry_on_database.description = entry_from_xml.description
    else:
        entry_on_database.description = html.escape(entry_from_xml.description)

    entry_on_database.save()


def poll_feed(feed_from_database, verbose=False):
    feed_from_xml = feedparser.parse(feed_from_database.xml_url)
    updated_feed = update_feed_on_database(feed_from_database, feed_from_xml, verbose)

    if updated_feed:
        if verbose:
            print(
                f"{len(feed_from_xml.entries)} entries to process in {updated_feed.title}"
            )

        entries_from_xml = feed_from_xml.entries[: settings.MAX_ENTRIES_SAVED]

        for i, entry_from_xml in enumerate(entries_from_xml):
            if skip_entry(entry_from_xml, verbose):
                continue

            entry_on_database, created = Entry.objects.get_or_create(
                feed=updated_feed, link=entry_from_xml.link
            )

            if created:
                update_entry_on_database(entry_on_database, entry_from_xml)
