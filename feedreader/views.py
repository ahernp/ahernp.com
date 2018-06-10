from django.views.generic.list import ListView

from datetime import datetime, timedelta

from django.conf import settings

from .models import Entry, Feed


def count_entries(entries):
    group_counts = {}
    feed_counts = {}
    non_group_count = 0
    for entry in entries:
        if entry.feed_id in feed_counts:
            feed_counts[entry.feed_id] += 1
        else:
            feed_counts[entry.feed_id] = 1
        if entry.feed.group_id:
            if entry.feed.group_id in group_counts:
                group_counts[entry.feed.group_id] += 1
            else:
                group_counts[entry.feed.group_id] = 1
        else:
            non_group_count += 1
    groups = Groups.objects.all()
    feeds = Entry.objects.all()
    counts = [
        {
            "group": group,
            "count": group_counts[group.id],
            "feeds": [
                {"feed": feed, "count": feed_counts[feed.id]}
                for feed in feeds
                if feed.group_id == group.id
            ],
        }
        for group in groups
    ]
    counts.append(
        {
            "group": None,
            "count": non_group_counts,
            "feeds": [
                {"feed": feed, "count": feed_counts[feed.id]}
                for feed in feeds
                if feed.group_id == None
            ],
        }
    )
    return counts


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
        context["counts"] = count_entries(self.queryset)
        return context
