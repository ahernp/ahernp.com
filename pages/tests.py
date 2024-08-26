import pytest
from django.urls import reverse

from .factories import PageFactory


@pytest.mark.django_db
def test_list_view(client):
    PageFactory.create()
    response = client.get(reverse("page-list"))
    assert response.status_code == 200
    assert b"<title>Pages</title>" in response.content


@pytest.mark.django_db
def test_detail_view(client):
    page = PageFactory.create()
    response = client.get(reverse("page-detail", kwargs={"slug": page.slug}))
    assert response.status_code == 200
    assert bytes(f"<title>{page.title}</title>", "utf-8") in response.content


@pytest.mark.django_db
def test_list_filter_view(client):
    parent = PageFactory.create()
    PageFactory.create(parent=parent)
    response = client.get(
        reverse("page-list-filter", kwargs={"parent_slug": parent.slug})
    )
    assert response.status_code == 200
    assert bytes(f"<title>{parent.title} Pages</title>", "utf-8") in response.content
    assert bytes(f"<h1>{parent.title} Pages</h1>", "utf-8") in response.content


def test_markdown_to_html():
    page = PageFactory.build(content="# Header")
    assert (
        page.content_as_html == '<h1 id="header">Header</h1>'
    ), "Expected content to be convertable to html"
