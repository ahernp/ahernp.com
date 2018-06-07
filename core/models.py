from datetime import timedelta

from django.db import models
from django.utils import timezone

RECENT = timedelta(days=1)


class Log(models.Model):
    level = models.CharField(max_length=10)
    msg = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return "{level} - {msg}...".format(level=self.level, msg=self.msg[:20])

    def recent(self):
        now = timezone.now()
        recent = self.datetime > (now - RECENT)
        return recent
