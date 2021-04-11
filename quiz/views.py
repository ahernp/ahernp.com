from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Quiz


class QuizListView(ListView):
    model = Quiz


class QuizDetailView(DetailView):
    model = Quiz

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = context["object"]
        topics = []
        questions_by_topic = {}
        for question in quiz.question_set.all():
            if question.topic not in topics:
                topics.append(question.topic)
            if question.topic.id not in questions_by_topic:
                questions_by_topic[question.topic.id] = []
            questions_by_topic[question.topic.id].append(question)
        context["topics"] = [
            {"topic": topic, "questions": questions_by_topic[topic.id]}
            for topic in topics
        ]
        return context
