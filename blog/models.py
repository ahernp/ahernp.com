from django.db import models

from mpages.models import Page


class BlogPage(Page):
    published = models.DateField(
        verbose_name="Date Published", null=True, blank=True, help_text="dd/mm/yyyy"
    )

    class Meta:
        app_label = "blog"
