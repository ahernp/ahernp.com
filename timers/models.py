from django.db import models


class Timer(models.Model):
    target = models.DateTimeField()
    label = models.TextField()
    slug = models.SlugField(max_length=250)

    class Meta:
        ordering = ["target"]

    def __str__(self):
        return self.label
