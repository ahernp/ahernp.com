import pytest

from django.urls import reverse

from .factories import BlogPageFactory


@pytest.mark.django_db
def test_list_view(client):
    blog_page = BlogPageFactory.create()
    response = client.get(reverse("blogpage-list"))
    assert response.status_code == 200
    assert b"<title>Blog</title>" in response.content


@pytest.mark.django_db
def test_detail_view(client):
    blog_page = BlogPageFactory.create()
    response = client.get(reverse("blogpage-detail", kwargs={"slug": blog_page.slug}))
    assert response.status_code == 200
    assert bytes(f"<title>{blog_page.title}</title>", "utf-8") in response.content
    assert (
        bytes(
            f'<h2 class="published-date">Published {blog_page.published.strftime("%Y-%m-%d")}</h2>',
            "utf-8",
        )
        in response.content
    )


@pytest.mark.django_db
def test_rss_feed_view(client):
    blog_page = BlogPageFactory.create()
    response = client.get(reverse("blog-rss-feed"))
    assert response.status_code == 200
    assert b'<rss version="2.0"' in response.content
    assert b"<title>ahernp.com blog</title>" in response.content
