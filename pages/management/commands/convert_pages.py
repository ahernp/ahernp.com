"""
This command copies old Pages and converts them into Markdown format.
"""
import json
from django.conf import settings
from django.core.management.base import BaseCommand

from pages.models import Page as OldPage
from mpages.models import Page as NewPage
from blog.models import BlogPage

import logging

logger = logging.getLogger(__name__)


def migrate_page(old_page, parent, blog=False):
    if old_page.content_type == "gallery":
        page = convert_gallery_to_markdown(old_page)
    else:
        page = old_page
    if blog:
        new_page = BlogPage.objects.create(
            title=page.title,
            slug=page.slug,
            content=page.content,
            updated=page.updated,
            parent=parent,
            published=page.published,
        )
    else:
        new_page = NewPage.objects.create(
            title=page.title,
            slug=page.slug,
            content=page.content,
            updated=page.updated,
            parent=parent,
        )
    new_page.save()
    return new_page


def convert_gallery_to_markdown(page):
    try:
        gallery = json.loads(page.content)
        markdown = ""
        for image in gallery["images"]:
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

        def update_caches(old_page):
            if old_page.slug in new_pages_cache or old_page.slug in new_blogpages_cache:
                return
            if old_page.parent.slug == settings.BLOG_ROOT_SLUG:
                new_blogpages_cache[old_page.slug] = migrate_page(
                    old_page, new_pages_cache[settings.BLOG_ROOT_SLUG], blog=True
                )
            else:
                new_pages_cache[old_page.slug] = migrate_page(
                    old_page, new_pages_cache[old_page.parent.slug]
                )

        if settings.HOMEPAGE_SLUG not in new_pages_cache:
            old_page = OldPage.objects.get(slug=settings.HOMEPAGE_SLUG)
            new_pages_cache[old_page.slug] = migrate_page(old_page, None)
            homepage = new_pages_cache[old_page.slug]
            homepage.parent = homepage
            homepage.save()
        else:
            homepage = new_pages_cache[settings.HOMEPAGE_SLUG]

        if settings.BLOG_ROOT_SLUG not in new_pages_cache:
            old_page = OldPage.objects.get(slug=settings.BLOG_ROOT_SLUG)
            new_pages_cache[old_page.slug] = migrate_page(old_page, None)
            blog_root = new_pages_cache[old_page.slug]
            blog_root.parent = blog_root
            blog_root.save()

        parent_ids = list(
            OldPage.objects.order_by("parent_id")
            .distinct()
            .values_list("parent_id", flat=True)
        )

        parents = OldPage.objects.filter(id__in=parent_ids).select_related("parent")

        # Add reference and linux parent pages first
        reference = OldPage.objects.get(slug="reference")
        update_caches(reference)
        linux = OldPage.objects.get(slug="linux")
        update_caches(linux)

        for old_page in parents:
            update_caches(old_page)

        old_pages = OldPage.objects.all().select_related("parent")

        for old_page in old_pages:
            update_caches(old_page)

        orphans = NewPage.objects.filter(parent=None)
        for orphan in orphans:
            orphan.parent = homepage
            orphan.save()
