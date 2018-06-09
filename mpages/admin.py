from django.contrib import admin

from .models import Page


class PageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "parent", "updated"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["updated"]
    ordering = ["parent", "title"]
    save_on_top = True
    fieldsets = (
        (None, {"fields": (("content",), ("title", "parent"), ("slug", "updated"))}),
    )


admin.site.register(Page, PageAdmin)
