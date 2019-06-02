from django.db import models
from django.urls import reverse


class Timer(models.Model):
    target = models.DateTimeField()
    label = models.TextField()
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ["target"]

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse("timer-detail", kwargs={"slug": self.slug})
