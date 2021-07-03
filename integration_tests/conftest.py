import pytest

from selenium.webdriver.chrome.options import Options
from selenium import webdriver


@pytest.fixture(scope="module")
def browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    options.experimental_options["prefs"] = chrome_prefs
    browser = webdriver.Chrome(options=options)

    yield browser
    browser.quit()
