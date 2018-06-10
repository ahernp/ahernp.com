from django.views.generic.list import ListView

from datetime import datetime, timedelta

from django.conf import settings

from .models import Entry


class EntryListView(ListView):
    model = Entry

    def get_queryset(self):
        from_time = datetime.utcnow() - timedelta(days=settings.MAX_DAYS_SHOWN)
        return Entry.objects.filter(published_time__gt=from_time).order_by(
            "-published_time"
        )[: settings.MAX_ENTRIES_SHOWN]
