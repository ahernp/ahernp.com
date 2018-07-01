from django.contrib import admin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = ["level", "datetime", "msg"]
    list_filter = ["level"]
    search_fields = ["msg"]
    readonly_fields = ["level", "datetime", "msg"]
    fieldsets = ((None, {"fields": (("level", "datetime"), ("msg",))}),)


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = "action_time"
    readonly_fields = [field.name for field in LogEntry._meta.fields] + [
        "object_link",
        "action_description",
    ]
    list_filter = ["user", "content_type", "action_flag"]
    search_fields = ["object_repr", "change_message"]
    list_display = [
        "action_time",
        "user",
        "content_type",
        "object_link",
        "action_description",
        "change_message",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != "POST"

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            admin_reference = f"admin:{ct.app_label}_{ct.model}_change"
            admin_link = reverse(admin_reference, args=[obj.object_id])
            link = f'<a href="{admin_link}">{escape(obj.object_repr)}</a>'
        return mark_safe(link)

    object_link.allow_tags = True
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"

    def action_description(self, obj):
        action_names = {ADDITION: "Addition", DELETION: "Deletion", CHANGE: "Change"}
        return action_names[obj.action_flag]

    action_description.short_description = "Action"


admin.site.register(Log, LogAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
