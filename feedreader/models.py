from django.db import models
from django.urls import reverse


class Group(models.Model):
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Feed(models.Model):
    title = models.CharField(max_length=2000, blank=True, null=True)
    xml_url = models.CharField(max_length=255, unique=True)
    link = models.CharField(max_length=2000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    published_time = models.DateTimeField(blank=True, null=True)
    last_polled_time = models.DateTimeField(blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    always_load = models.BooleanField(default=False)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title or self.xml_url

    def save(self, *args, **kwargs):
        try:
            Feed.objects.get(xml_url=self.xml_url)
            super(Feed, self).save(*args, **kwargs)
        except Feed.DoesNotExist:
            super(Feed, self).save(*args, **kwargs)
            from feedreader.utils import poll_feed

            poll_feed(self, initial=True)

    def get_absolute_url(self):
        return reverse("feed-recent-entries", kwargs={"feed_id": self.id})


class Entry(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000, blank=True, null=True)
    link = models.CharField(max_length=2000)
    media_link = models.CharField(max_length=2000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    published_time = models.DateTimeField(auto_now_add=True)
    read_flag = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_time"]
        verbose_name_plural = "entries"

    def __str__(self):
        return self.title

    @property
    def media_name(self):
        if self.media_link:
            return self.media_link.split("/")[-1]
        return ""
