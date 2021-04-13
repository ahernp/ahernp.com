from django.db import models
from django.urls import reverse

ANSWER_CHOICES = (
    ("a", "A"),
    ("b", "B"),
    ("c", "C"),
    ("d", "D"),
)


class Quiz(models.Model):
    title = models.TextField()
    show_answers = models.BooleanField()

    class Meta:
        verbose_name_plural = "Quizes"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("quiz-detail", kwargs={"pk": self.id})


class Topic(models.Model):
    title = models.TextField()

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.TextField()
    answer_a = models.TextField()
    answer_b = models.TextField()
    answer_c = models.TextField()
    answer_d = models.TextField()
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["quiz", "topic", "question"]

    def __str__(self):
        return self.question
