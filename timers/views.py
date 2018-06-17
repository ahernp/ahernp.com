from django.views.generic.base import TemplateView


class TimersListView(TemplateView):
    template_name = "timers/index.html"
