from django.db import models
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

import markdown

MARKDOWN_EXTENSIONS = ['extra', 'tables', 'toc']


class Page(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    updated = models.DateTimeField(verbose_name="Time Updated", auto_now=True)
    content = models.TextField(verbose_name="Page content", blank=True)

    @property
    def content_as_html(self):
        return mark_safe(markdown.markdown(force_text(self.content),
                                           MARKDOWN_EXTENSIONS,
safe_mode=False))

    class Meta:
        app_label = "mpages"
        ordering = ["title"]

    def __str__(self):
        return self.title
