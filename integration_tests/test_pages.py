import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By

from pages.factories import PageFactory

PAGE_TITLE = "Page Title"


@pytest.mark.django_db
def test_page_list(browser, live_server):
    PageFactory.create()
    relative_url = reverse("page-list")
    browser.get(f"{live_server.url}{relative_url}")

    h1 = browser.find_element(By.CSS_SELECTOR, "h1")
    assert h1.text == "Pages"

    datatables_footer = browser.find_element(By.ID, "DataTables_Table_0_info")
    assert datatables_footer.text == "Showing 1 to 1 of 1 entries"


@pytest.mark.django_db
def test_page_detail(browser, live_server):
    page = PageFactory.create(content=f"# {PAGE_TITLE}")
    relative_url = reverse("page-detail", kwargs={"slug": page.slug})
    browser.get(f"{live_server.url}{relative_url}")

    h1 = browser.find_element(By.CSS_SELECTOR, "h1")
    assert h1.text == PAGE_TITLE
