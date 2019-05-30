from django.contrib import admin

from mpages.admin import PageAdmin
from .models import BlogPage


class BlogPageAdmin(PageAdmin):
    list_display = ["title", "parent", "updated", "published"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("content",),
                    ("title", "parent"),
                    ("published", "updated"),
                    ("slug"),
                )
            },
        ),
    )
    autocomplete_fields = ["parent"]


admin.site.register(BlogPage, BlogPageAdmin)
