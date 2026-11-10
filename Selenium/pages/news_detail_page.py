from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class NewsDetailPage(BasePage):
    URL_PATH = "/news/{slug}/"

    HERO_HEADING = (By.CSS_SELECTOR, ".page-hero-navy h1")

    def load(self, base_url, slug):
        path = self.URL_PATH.format(slug=slug)
        self.driver.get(f"{base_url.rstrip('/')}{path}")
        self.force_aos_visible()
        return self

    def get_title(self):
        return self.get_text(self.HERO_HEADING)
