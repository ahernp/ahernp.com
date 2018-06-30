from django.conf import settings
from django.contrib.syndication.views import Feed

from .models import BlogPage


class LatestBlogPostsFeed(Feed):
    title = f"{settings.SITE_NAME} blog"
    link = "/blog/"
    description = "Recent Blog Entries."

    def items(self):
        return BlogPage.objects.all().order_by("-published")[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if len(item.content) > 100:
            para_end = item.content.find("\n", 100)
            if para_end > 0:
                return f"{item.content[:para_end]}..."
        return item.content

    def item_pubdate(self, item):
        return item.updated

    def item_link(self, item):
        return f"/pages/{item.slug}/"
