from django.contrib import admin

from .models import Group, Feed, Entry


class FeedAdmin(admin.ModelAdmin):
    list_display = ["xml_url", "title", "group", "published_time", "last_polled_time"]
    list_filter = ["group"]
    search_fields = ["link", "title"]
    readonly_fields = [
        "title",
        "link",
        "description",
        "published_time",
        "last_polled_time",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("xml_url", "group"),
                    ("title", "link"),
                    ("description",),
                    ("published_time", "last_polled_time"),
                )
            },
        ),
    )


def mark_as_read(modeladmin, request, queryset):
    queryset.update(read_flag=True)


mark_as_read.short_description = "Mark selected entries as read"


class EntryAdmin(admin.ModelAdmin):
    list_display = ["title", "feed", "published_time"]
    list_filter = ["read_flag", "feed"]
    search_fields = ["title", "link"]
    actions = [mark_as_read]
    readonly_fields = [
        "link",
        "media_link",
        "title",
        "description",
        "published_time",
        "feed",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("link",),
                    ("media_link",),
                    ("title", "feed"),
                    ("description",),
                    ("published_time", "read_flag"),
                )
            },
        ),
    )


admin.site.register(Group)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Entry, EntryAdmin)
