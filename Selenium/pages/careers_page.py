from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CareersPage(BasePage):
    URL_PATH = "/careers/"

    HERO_HEADING = (By.CSS_SELECTOR, ".page-hero-careers h1")
    JOB_CARDS = (By.CSS_SELECTOR, ".job-card")
    JOB_TITLES = (By.CSS_SELECTOR, ".job-card h3")
    CTA_BUTTON = (By.CSS_SELECTOR, ".careers-cta a.btn-arrow-circle")
    JOB_APPLY_XPATH = "(//div[contains(@class,'job-card')]//a[contains(@class,'btn-arrow-circle')])[{n}]"

    STORIES_SECTION = (By.CSS_SELECTOR, "section.employee-stories")
    STORIES_TRACK = (By.ID, "storiesTrack")
    STORY_SLOTS = (By.CSS_SELECTOR, "#storiesTrack .story-slot")
    ACTIVE_STORY = (By.CSS_SELECTOR, "#storiesTrack .story-slot-active")
    STORY_AUTHOR_NAME = (By.ID, "storyAuthorName")
    STORY_AUTHOR_ROLE = (By.ID, "storyAuthorRole")

    def load(self, base_url):
        self.driver.get(f"{base_url.rstrip('/')}{self.URL_PATH}")
        self.force_aos_visible()
        return self

    def get_hero_heading(self):
        return self.get_text(self.HERO_HEADING)

    def get_job_card_count(self):
        return len(self.find_all(self.JOB_CARDS))

    def open_job(self, index=0):
        current_url = self.driver.current_url
        locator = (By.XPATH, self.JOB_APPLY_XPATH.format(n=index + 1))
        self.click(locator)
        if self.wait_for_navigation(current_url):
            self.force_aos_visible()
        return self

    def is_stories_section_visible(self):
        return self.is_visible(self.STORIES_SECTION)

    def get_story_slot_count(self):
        return len(self.find_all(self.STORY_SLOTS))

    def get_active_story_text(self):
        return self.get_text(self.ACTIVE_STORY)

    def get_track_offset_x(self):
        return self.driver.execute_script(
        "return new DOMMatrix(getComputedStyle(arguments[0]).transform).m41;",
        self.find(self.STORIES_TRACK),
    )
    def get_job_titles(self):
        return [el.text.strip() for el in self.find_all(self.JOB_TITLES)]

    def get_story_author_name(self):
        return self.get_text(self.STORY_AUTHOR_NAME)

    def get_story_author_role(self):
        return self.get_text(self.STORY_AUTHOR_ROLE)

    def open_general_application(self):
        current_url = self.driver.current_url
        self.click(self.CTA_BUTTON)
        if self.wait_for_navigation(current_url):
            self.force_aos_visible()
            return self
    