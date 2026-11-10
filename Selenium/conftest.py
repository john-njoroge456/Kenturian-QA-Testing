import os

import pytest
from selenium import webdriver

BASE_URL = "http://127.0.0.1:9000"

# Set HEADLESS=1 to run Chrome without a window, e.g. where a desktop
# session isn't available. The window size stays the same either way.
HEADLESS = os.environ.get("HEADLESS") == "1"


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1366,768")
    if HEADLESS:
        options.add_argument("--headless=new")
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


@pytest.fixture
def base_url():
    return BASE_URL