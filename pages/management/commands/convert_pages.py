"""
This command copies old Pages and converts them into Markdown format.
"""
import json
from django.core.management.base import BaseCommand

from pages.models import Page as OldPage
from mpages.models import Page as NewPage
from blog.models import Page as BlogPage

import logging

logger = logging.getLogger(__name__)

HOMEPAGE_SLUG = 'ahernp-com'
BLOG_ROOT_SLUG = 'blog'


def migrate_page(old_page, parent):
    new_page = NewPage.objects.create(
        title=old_page.title,
        slug=old_page.slug,
        content=old_page.content,
        updated=old_page.updated,
        parent=parent
    )
    new_page.save()
    return new_page


def convert_gallery_to_markdown(page):
    try:
        gallery = json.loads(page.content)
        markdown = ""
        for image in gallery["images"]:
            print(image)
            image_markdown = '[![{title}](https://ahernp.com{thumbnailUrl} "{title}")](https://ahernp.com{imageUrl})'.format(
                title=image["title"],
                imageUrl=image["imageUrl"],
                thumbnailUrl=image["thumbnailUrl"],
            )
            markdown += image_markdown + "\n"
        page.content = markdown
        return page
    except json.decoder.JSONDecodeError:
        print("JSONDecodeError", page.id)


class Command(BaseCommand):
    help = "Convert Pages into Markdown and BlogPages."

    def handle(self, *args, **options):
        new_pages_cache = {page.slug: page for page in NewPage.objects.all()}
        new_blogpages_cache = {page.slug: page for page in BlogPage.objects.all()}

        if HOMEPAGE_SLUG not in new_pages_cache:
            old_page = OldPage.objects.get(slug=HOMEPAGE_SLUG)
            new_pages_cache[old_page.slug] = migrate_page(old_page, None)

        if BLOG_ROOT_SLUG not in new_pages_cache:
            old_page = OldPage.objects.get(slug=BLOG_ROOT_SLUG)
            new_blogpages_cache[old_page.slug] = migrate_page(old_page, None)

        oldpages = OldPage.objects.all()

        for oldpage in oldpages:
            page = oldpage
            if page.slug in new_pages_cache or page.slug in new_blogpages_cache:
                continue
            if oldpage.content_type == "gallery":
                page = convert_gallery_to_markdown(page)
                new_pages_cache[page.slug] = migrate_page(page, new_pages_cache[HOMEPAGE_SLUG])
            elif oldpage.parent.slug == BLOG_ROOT_SLUG:
                new_blogpages_cache[page.slug] = migrate_page(page, new_pages_cache[BLOG_ROOT_SLUG])
            else:
                new_pages_cache[page.slug] = migrate_page(page, new_pages_cache[HOMEPAGE_SLUG])
