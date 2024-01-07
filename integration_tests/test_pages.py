import time

import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By

from pages.factories import PageFactory
from pages.models import Page

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


@pytest.mark.django_db
def test_page_edit(admin_client_browser, live_server):
    page = PageFactory.create(content=f"# {PAGE_TITLE}")
    relative_url = reverse("page-detail", kwargs={"slug": page.slug})
    admin_client_browser.get(f"{live_server.url}{relative_url}")
    admin_client_browser.find_element(By.LINK_TEXT, "Edit").click()

    h1 = admin_client_browser.find_element(By.CSS_SELECTOR, "h1")
    assert h1.text == "Edit Markdown"

    # Edit page content
    textarea = admin_client_browser.find_element(By.ID, "markdown")
    textarea.clear()
    edited_content = f"## {PAGE_TITLE}"
    textarea.send_keys(edited_content)

    # Preview edited page content
    admin_client_browser.find_element(By.ID, "preview-button").click()
    h2 = admin_client_browser.find_element(By.CSS_SELECTOR, "h2")
    assert h2.text == PAGE_TITLE

    # Save edited page content
    admin_client_browser.find_element(By.XPATH, '//button[text()="Save"]').click()
    time.sleep(1)  # Wait for change to be saved to database
    page_from_database = Page.objects.get(pk=page.id)
    assert page_from_database.content == edited_content
