from django.contrib import admin

from .models import Timer


class TimerAdmin(admin.ModelAdmin):
    search_fields = ["label"]
    list_display = ["label", "target"]
    prepopulated_fields = {"slug": ("label",)}


admin.site.register(Timer, TimerAdmin)
