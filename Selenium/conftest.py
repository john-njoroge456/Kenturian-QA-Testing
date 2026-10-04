import pytest
from selenium import webdriver

BASE_URL = "http://127.0.0.1:9000"


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    drv = webdriver.Chrome(options=options)
    drv.maximize_window()
    yield drv
    drv.quit()


@pytest.fixture
def base_url():
    return BASE_URL