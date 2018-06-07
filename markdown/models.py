from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(verbose_name="Time Updated", auto_now=True)
    content = models.TextField(verbose_name="Page content", blank=True)

    class Meta:
        app_label = "markdown"
        ordering = ["title"]

    def __str__(self):
        return self.title
