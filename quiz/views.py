from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Quiz


class QuizListView(ListView):
    model = Quiz


class QuizDetailView(DetailView):
    model = Quiz
