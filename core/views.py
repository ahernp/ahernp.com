from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F
from django.views.generic.base import TemplateView

from .utils import Headline
from feedreader.models import Entry
from mpages.models import Page


class SearchView(TemplateView):
    template_name = "core/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_string = self.request.GET.get("search", "")
        if len(search_string) >= 3:
            pages = Page.objects.all()
            entries = Entry.objects.all()

            search_query = SearchQuery(search_string)
            title_vector = SearchVector('title', weight='A')
            content_vector = SearchVector('content', weight='B')
            description_vector = SearchVector('description', weight='B')
            page_vectors = title_vector + content_vector
            entry_vectors = title_vector + description_vector

            pages = pages.annotate(search=page_vectors).filter(search=search_query)
            pages = pages.annotate(rank=SearchRank(page_vectors, search_query)).order_by('-rank')
            pages = pages.annotate(title_highlight=Headline(F('title'), search_query))
            pages = pages.annotate(content_highlight=Headline(F('content'), search_query))
            context["pages"] = pages

            entries = entries.annotate(search=entry_vectors).filter(search=search_query)
            entries = entries.annotate(rank=SearchRank(entry_vectors, search_query)).order_by('-rank')
            entries = entries.annotate(title_highlight=Headline(F('title'), search_query))
            entries = entries.annotate(description_highlight=Headline(F('description'), search_query))
            context["entries"] = entries
        else:
            context["error"] = "Search term must be at least 3 characters"
        context["search_string"] = search_string
        return context
