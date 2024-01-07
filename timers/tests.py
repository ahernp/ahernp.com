import pytest
from django.urls import reverse

from .factories import TimerFactory


@pytest.mark.django_db
def test_timers(client):
    timer = TimerFactory.create()
    response = client.get(reverse("timers"))
    assert response.status_code == 200
    assert b"<title>Timers</title>" in response.content
    assert bytes(f'label="{timer.label}"', "utf-8") in response.content
