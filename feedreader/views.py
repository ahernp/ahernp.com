import collections
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from django.conf import settings

from .models import Entry, Feed, Group


class FeedCount(object):
    total_count = 0
    unread_count = 0

    def __init__(self, feed):
        self.feed = feed


class GroupCount(object):
    total_count = 0
    unread_count = 0
    feed_counts = []

    def __init__(self, group):
        self.group = group


def count_entries(groups, feeds, entries):
    group_counts = collections.OrderedDict(
        [(group.id, GroupCount(group=group)) for group in groups]
    )
    feed_counts = collections.OrderedDict(
        [(feed.id, FeedCount(feed=feed)) for feed in feeds]
    )

    for entry in entries:
        feed_counts[entry.feed_id].total_count += 1
        if not entry.read_flag:
            feed_counts[entry.feed_id].unread_count += 1
        if entry.feed.group_id:
            group_counts[entry.feed.group_id].total_count += 1
            if not entry.read_flag:
                group_counts[entry.feed.group_id].unread_count += 1

    total_entries = len(entries)
    total_unread = 0
    non_group_feed_counts = []

    for _, feed_count in feed_counts.items():
        if feed_count.feed.group_id:
            group_counts[feed_count.feed.group_id].feed_counts.append(feed_count)
        else:
            non_group_feed_counts.append(feed_counts)
            total_unread += feed_count.unread_count

    return {
        "group_counts": list(group_counts.values()),
        "non_group_feed_counts": non_group_feed_counts,
        "total_entries": total_entries,
        "total_unread": total_unread,
    }


class EntryListView(ListView):
    model = Entry

    def get_queryset(self):
        from_time = datetime.utcnow() - timedelta(days=settings.MAX_DAYS_SHOWN)
        feed_id = self.kwargs.get("feed_id", None)
        if feed_id:
            self.feed = get_object_or_404(Feed, id=feed_id)
            return Entry.objects.filter(
                published_time__gt=from_time, feed=self.feed
            ).order_by("-published_time")[: settings.MAX_ENTRIES_SHOWN]
        self.feed = None
        return Entry.objects.filter(published_time__gt=from_time).order_by(
            "-published_time"
        )[: settings.MAX_ENTRIES_SHOWN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed"] = self.feed
        groups = Group.objects.all()
        feeds = Feed.objects.all()
        context["counts"] = count_entries(groups, feeds, self.queryset)
        return context
