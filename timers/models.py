from django.db import models


class Timer(models.Model):
    target = models.DateTimeField()
    label = models.TextField()

    class Meta:
        ordering = ["target"]

    def __str__(self):
        return self.label
