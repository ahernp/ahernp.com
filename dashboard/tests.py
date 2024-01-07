import pytest
from django.urls import reverse

from .views import project_state_at_startup


@pytest.mark.django_db
def test_dashboard(client):
    response = client.get(reverse("dashboard"))
    assert response.status_code == 200
    assert b"<title>Dashboard</title>" in response.content


def test_project_state_at_startup():
    project_state = project_state_at_startup()
    assert type(project_state) == dict
    assert len(project_state) == 6
