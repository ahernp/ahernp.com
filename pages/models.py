import markdown
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe


class Page(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    updated = models.DateTimeField(verbose_name="Time Updated", auto_now=True)
    content = models.TextField(verbose_name="Page content", blank=True)

    @property
    def content_as_html(self):
        return mark_safe(
            markdown.markdown(
                force_str(self.content),
                extensions=settings.MARKDOWN_EXTENSIONS,
            )
        )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("page-detail", kwargs={"slug": self.slug})
