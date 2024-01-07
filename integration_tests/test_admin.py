import pytest
from selenium.webdriver.common.by import By


@pytest.mark.django_db
def test_admin(admin_client_browser, live_server):
    url = f"{live_server.url}/admin/"
    admin_client_browser.get(url)

    h1 = admin_client_browser.find_element(By.TAG_NAME, "h1")
    assert h1.text == "Django administration"
    assert admin_client_browser.current_url == url
