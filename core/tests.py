import datetime

import pytest
from django.urls import reverse
from django.utils import timezone

from pages.factories import PageFactory

from .factories import LogFactory


@pytest.mark.django_db
def test_search(client):
    page = PageFactory.create()
    response = client.get(f'{reverse("search")}?search=page')
    assert response.status_code == 200
    assert b"<title>Search Results</title>" in response.content
    assert bytes(f'<a href="{page.get_absolute_url()}">', "utf-8") in response.content


def test_upload_page_requires_login(client, admin_client):
    response = client.get(reverse("upload"), follow=True)
    assert response.status_code == 200
    assert b"<title>Log in | Django site admin</title>" in response.content

    response = admin_client.get(reverse("upload"))
    assert response.status_code == 200
    assert b"<title>Upload Files</title>" in response.content


def test_recent_logs():
    log = LogFactory.create()
    assert log.recent() is True, "Newly created log is recent"

    log.datetime = timezone.now() - datetime.timedelta(days=2)
    assert log.recent() is False, "Two day old log is not recent"
