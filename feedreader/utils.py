from datetime import datetime, timedelta
from time import mktime

import logging
import feedparser
import pytz

from django.conf import settings
from django.utils import html
from django.utils import timezone

from .models import Entry

logger = logging.getLogger(__name__)

AGE_WINDOW = timedelta(days=settings.MAX_DAYS_AGE)


def log_and_display_message(message, verbose=False):
    logger.error(message)
    if verbose:
        print(message)


def get_xml_time(xml_object):
    xml_time = None

    if hasattr(xml_object, "feed"):
        if hasattr(xml_object.feed, "published_parsed"):
            xml_time = xml_object.feed.published_parsed
        elif hasattr(xml_object.feed, "updated_parsed"):
            xml_time = xml_object.feed.updated_parsed
        elif len(xml_object.entries) > 0:
            if hasattr(xml_object.entries[0], "published_parsed"):
                xml_time = xml_object.entries[0].published_parsed
            elif hasattr(xml_object.entries[0], "updated_parsed"):
                xml_time = xml_object.entries[0].updated_parsed
    else:
        if hasattr(xml_object, "published_parsed"):
            xml_time = xml_object.published_parsed
        elif hasattr(xml_object, "updated_parsed"):
            xml_time = xml_object.updated_parsed

    if xml_time is not None:
        xml_time = datetime.fromtimestamp(mktime(xml_time))

        try:
            xml_time = pytz.timezone(settings.TIME_ZONE).localize(xml_time, is_dst=None)
        except pytz.exceptions.AmbiguousTimeError:
            pytz_timezone = pytz.timezone(settings.TIME_ZONE)
            xml_time = pytz_timezone.localize(xml_time, is_dst=False)

    return xml_time


def update_feed_on_database(feed_from_database, feed_from_xml, initial, verbose):
    if hasattr(feed_from_xml.feed, "bozo_exception"):
        message = (
            f"Feedreader poll_feeds found Malformed feed, "
            f'"{feed_from_database.xml_url}": '
            f"{feed_from_xml.feed.bozo_exception}"
        )
        log_and_display_message(message, verbose)
        return

    xml_time = get_xml_time(feed_from_xml)

    if xml_time is None:
        log_and_display_message(
            f'Feedreader poll_feeds. Feed "{feed_from_database.xml_url}" has no published or updated time',
            verbose,
        )
        return

    if (
        not initial
        and feed_from_database.published_time
        and feed_from_database.published_time >= xml_time
    ):
        return

    feed_from_database.published_time = xml_time

    for attr in ["title", "title_detail"]:
        if not hasattr(feed_from_xml.feed, attr):
            log_and_display_message(
                f'Feedreader poll_feeds. Feed "{feed_from_database.xml_url}" has no {attr}',
                verbose,
            )
            return

    if feed_from_xml.feed.title_detail.type == "text/plain":
        feed_from_database.title = html.escape(feed_from_xml.feed.title)
    else:
        feed_from_database.title = feed_from_xml.feed.title

    if hasattr(feed_from_xml.feed, "link"):
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


def skip_entry(entry_from_xml, initial=False, verbose=False):
    for attr in ["title", "title_detail", "links", "description"]:
        if not hasattr(entry_from_xml, attr):
            log_and_display_message(
                f"Feedreader poll_feeds. Entry has no {attr}: {entry_from_xml}", verbose
            )
            return True

    if len(entry_from_xml.links) == 0:
        log_and_display_message(
            f"Feedreader poll_feeds. Entry has an empty list of links: {entry_from_xml}",
            verbose,
        )
        return True

    if not hasattr(entry_from_xml.links[0], "href"):
        log_and_display_message(
            f"Feedreader poll_feeds. First links of Entry has no href: {entry_from_xml}",
            verbose,
        )
        return True

    if entry_from_xml.title == "":
        log_and_display_message(
            f"Feedreader poll_feeds. Entry has a blank title: {entry_from_xml}", verbose
        )
        return True

    xml_time = get_xml_time(entry_from_xml)

    if xml_time is None:
        log_and_display_message(
            f"Feedreader poll_feeds. Entry has a no published or updated time: {entry_from_xml}",
            verbose,
        )
        return True

    if not initial and (xml_time < (timezone.now() - AGE_WINDOW)):
        return True


def update_entry_on_database(entry_on_database, entry_from_xml):
    xml_time = get_xml_time(entry_from_xml)

    if xml_time is None:
        return

    entry_on_database.published_time = xml_time

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

    if hasattr(entry_from_xml, "links"):
        for link in entry_from_xml.links:
            if link.rel == "enclosure":
                entry_on_database.media_link = link.href
                break

    entry_on_database.read_flag = False

    entry_on_database.save()

    return entry_on_database


def poll_feed(feed_from_database, initial=False, verbose=False):
    feed_from_xml = feedparser.parse(feed_from_database.xml_url)
    entries_from_xml = feed_from_xml.entries[: settings.MAX_ENTRIES_SAVED]
    num_new_entries = 0

    if entries_from_xml:
        updated_feed = update_feed_on_database(
            feed_from_database, feed_from_xml, initial, verbose
        )

        if updated_feed:
            if verbose and feed_from_xml.entries:
                print(
                    f"{len(feed_from_xml.entries)} entries to process in {updated_feed.title}"
                )

            for entry_from_xml in entries_from_xml:
                if skip_entry(entry_from_xml, initial, verbose):
                    continue

                link = (
                    entry_from_xml.link
                    if hasattr(entry_from_xml, "link")
                    else entry_from_xml.links[0].href
                )

                entry_on_database, created = Entry.objects.get_or_create(
                    feed=updated_feed, link=link
                )

                if created:
                    updated_entry = update_entry_on_database(
                        entry_on_database, entry_from_xml
                    )
                    if updated_entry is not None:
                        num_new_entries += 1

    return num_new_entries
