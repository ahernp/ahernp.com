import pytest

from django.urls import reverse

from pages.factories import PageFactory


@pytest.mark.django_db
def test_home_page(browser, live_server):
    PageFactory.create()
    browser.get(f"{live_server.url}{reverse('page-list')}")

    h1 = browser.find_element_by_css_selector("h1")
    assert h1.text == "Pages"

    datatables_footer = browser.find_element_by_id("DataTables_Table_0_info")
    assert datatables_footer.text == "Showing 1 to 1 of 1 entries"
