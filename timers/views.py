from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Timer


class TimerDetailView(DetailView):
    model = Timer


class TimersListView(ListView):
    model = Timer
