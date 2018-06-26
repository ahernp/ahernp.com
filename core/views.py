from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from mpages.models import Page


def view_404(request):
    return redirect("homepage")


class SearchView(TemplateView):
    template_name = "core/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keywords = self.request.GET.get("search", "")
        if len(keywords) >= 3:
            pages = Page.objects.all()

            query = SearchQuery(keywords)
            title_vector = SearchVector('title', weight='A')
            content_vector = SearchVector('content', weight='B')
            vectors = title_vector + content_vector
            pages = pages.annotate(search=vectors).filter(search=query)
            pages = pages.annotate(rank=SearchRank(vectors, query)).order_by('-rank')
            context["pages"] = pages
        else:
            context["error"] = "Search term must be at least 3 characters"
        context["keywords"] = keywords
        return context
