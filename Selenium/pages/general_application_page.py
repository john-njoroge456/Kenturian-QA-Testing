from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class GeneralApplicationPage(BasePage):
    URL_PATH = "/careers/apply/"

    HERO_HEADING = (By.CSS_SELECTOR, ".page-hero-careers h1")
    HERO_SUBTITLE = (By.CSS_SELECTOR, ".page-hero-careers .lead")
    BREADCRUMB_LINKS = (By.CSS_SELECTOR, ".breadcrumb-text a.breadcrumb-link")

    NAME_INPUT = (By.ID, "id_name")
    EMAIL_INPUT = (By.ID, "id_email")
    PHONE_INPUT = (By.ID, "id_phone")
    MESSAGE_TEXTAREA = (By.ID, "id_message")
    CV_INPUT = (By.ID, "id_cv")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, ".application-form button[type='submit']")
    FORM_CARD = (By.CSS_SELECTOR, ".application-form-card")
    FORM_ERROR_NOTE = (By.CSS_SELECTOR, ".form-error-note")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".application-success-card h3")
    BACK_LINK = (By.PARTIAL_LINK_TEXT, "Back to all vacancies")

    def load(self, base_url):
        self.driver.get(f"{base_url.rstrip('/')}{self.URL_PATH}")
        self.force_aos_visible()
        return self

    def get_title(self):
        return self.get_text(self.HERO_HEADING)

    def get_subtitle(self):
        return self.get_text(self.HERO_SUBTITLE)

    def get_breadcrumb_texts(self):
        return [el.text.strip() for el in self.find_all(self.BREADCRUMB_LINKS)]

    def fill_form(self, name="", email="", phone="", message="", cv_path=""):
        if name:
            field_name = self.find(self.NAME_INPUT)
            field_name.clear()
            field_name.send_keys(name)
        if email:
            field_email = self.find(self.EMAIL_INPUT)
            field_email.clear()
            field_email.send_keys(email)
        if phone:
            field_phone = self.find(self.PHONE_INPUT)
            field_phone.clear()
            field_phone.send_keys(phone)
        if message:
            field_message = self.find(self.MESSAGE_TEXTAREA)
            field_message.clear()
            field_message.send_keys(message)
        if cv_path:
            self.find(self.CV_INPUT).send_keys(cv_path)
        return self

    def submit(self):
        current_url = self.driver.current_url
        self.click(self.SUBMIT_BUTTON)
        self.wait_for_navigation(current_url)
        self.force_aos_visible()
        return self

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MESSAGE)

    def get_form_error_note(self):
        return self.get_text(self.FORM_ERROR_NOTE)

    def is_form_visible(self):
        return self.is_visible(self.FORM_CARD, timeout=5)

    def go_back_to_vacancies(self):
        current_url = self.driver.current_url
        self.click(self.BACK_LINK)
        if self.wait_for_navigation(current_url):
            self.force_aos_visible()
        return self