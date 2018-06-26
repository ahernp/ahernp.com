from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F
from django.views.generic.base import TemplateView

from .utils import Headline
from mpages.models import Page


class SearchView(TemplateView):
    template_name = "core/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keywords = self.request.GET.get("search", "")
        if len(keywords) >= 3:
            pages = Page.objects.all()

            search_query = SearchQuery(keywords)
            title_vector = SearchVector('title', weight='A')
            content_vector = SearchVector('content', weight='B')
            vectors = title_vector + content_vector
            pages = pages.annotate(search=vectors).filter(search=search_query)
            pages = pages.annotate(rank=SearchRank(vectors, search_query)).order_by('-rank')
            pages = pages.annotate(title_highlight=Headline(F('title'), search_query))
            pages = pages.annotate(content_highlight=Headline(F('content'), search_query))
            context["pages"] = pages
        else:
            context["error"] = "Search term must be at least 3 characters"
        context["keywords"] = keywords
        return context
