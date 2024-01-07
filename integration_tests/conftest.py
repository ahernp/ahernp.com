import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_chrome_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    options.experimental_options["prefs"] = chrome_prefs
    return options


@pytest.fixture(scope="module")
def browser():
    browser = webdriver.Chrome(options=get_chrome_options())

    yield browser
    browser.quit()


@pytest.fixture
def admin_client_browser(admin_client, live_server):
    sessionid = admin_client.cookies["sessionid"]
    cookie = {
        "name": sessionid.key,
        "value": sessionid.value,
        "path": "/",
        "secure": False,
    }
    browser = webdriver.Chrome(options=get_chrome_options())
    browser.implicitly_wait(3)  # Wait for elements to appear
    browser.get(live_server.url)
    browser.delete_cookie("sessionid")
    browser.add_cookie(cookie)

    yield browser
    browser.quit()
