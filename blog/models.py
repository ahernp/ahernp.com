from django.db import models
from django.urls import reverse

from pages.models import Page


class BlogPage(Page):
    published = models.DateField(
        verbose_name="Date Published", null=True, blank=True, help_text="dd/mm/yyyy"
    )

    class Meta:
        ordering = ["-published"]

    def get_absolute_url(self):
        return reverse("blogpage-detail", kwargs={"slug": self.slug})
