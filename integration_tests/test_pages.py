import pytest

from django.urls import reverse

from pages.factories import PageFactory


@pytest.mark.django_db
def test_page_list(browser, live_server):
    PageFactory.create()
    relative_url = reverse("page-list")
    browser.get(f"{live_server.url}{relative_url}")

    h1 = browser.find_element_by_css_selector("h1")
    assert h1.text == "Pages"

    datatables_footer = browser.find_element_by_id("DataTables_Table_0_info")
    assert datatables_footer.text == "Showing 1 to 1 of 1 entries"


@pytest.mark.django_db
def test_page_detail(browser, live_server):
    PAGE_TITLE = "Page Title"
    page = PageFactory.create(content=f"# {PAGE_TITLE}")
    relative_url = reverse("page-detail", kwargs={"slug": page.slug})
    browser.get(f"{live_server.url}{relative_url}")

    h1 = browser.find_element_by_css_selector("h1")
    assert h1.text == PAGE_TITLE


@pytest.mark.django_db
def test_admin(admin_client_browser, live_server):
    url = f"{live_server.url}/admin/"
    admin_client_browser.get(url)

    h1 = admin_client_browser.find_element_by_css_selector("h1")
    assert h1.text == "Django administration"
    assert admin_client_browser.current_url == url
