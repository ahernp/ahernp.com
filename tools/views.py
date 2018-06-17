from django.views.generic.base import TemplateView


class ToolsView(TemplateView):
    template_name = "tools/index.html"
