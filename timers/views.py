from django.views.generic.list import ListView

from .models import Timer


class TimersListView(ListView):
    model = Timer
