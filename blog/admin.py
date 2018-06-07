from django.contrib import admin

from markdown.admin import PageAdmin
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


admin.site.register(BlogPage, BlogPageAdmin)
