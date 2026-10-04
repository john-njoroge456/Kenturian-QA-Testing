from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ContactPage(BasePage):
    URL_PATH = "/contact/"
    NAME_INPUT = (By.ID, "id_name")
    EMAIL_INPUT = (By.ID, "id_email")
    SUBJECT_INPUT = (By.ID, "id_subject")
    MESSAGE_TEXTAREA = (By.ID, "id_message")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button.btn-navy-arrow")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".application-success-card h3")

    OFFICE_INFO_CARD = (By.CSS_SELECTOR, ".contact-info-card")
    OFFICE_INFO_ITEMS = (By.CSS_SELECTOR, ".contact-info-item")
    PHONE_LINK = (By.CSS_SELECTOR, ".contact-info-item a[href^='tel:']")
    WHATSAPP_LINK = (By.CSS_SELECTOR, ".contact-info-item a[href^='https://wa.me/']")
    EMAIL_LINK = (By.CSS_SELECTOR, ".contact-info-item a[href^='mailto:']")
    MAP_IFRAME = (By.CSS_SELECTOR, ".contact-map-card iframe")
    def load(self, base_url):
        self.driver.get(f"{base_url.rstrip('/')}{self.URL_PATH}")
        self.force_aos_visible()
        return self
 
    def fill_form(self, name="", email="", subject="", message=""):
        if name:
            field_name=self.find(self.NAME_INPUT)
            field_name.clear()
            field_name.send_keys(name)
        if email:
            field_email=self.find(self.EMAIL_INPUT)
            field_email.clear()
            field_email.send_keys(email)
        if subject:
            field_subject=self.find(self.SUBJECT_INPUT)
            field_subject.clear()
            field_subject.send_keys(subject)
        if message:
            field_message=self.find(self.MESSAGE_TEXTAREA)
            field_message.clear()
            field_message.send_keys(message)
        return self
 
    def submit(self):
        current_url = self.driver.current_url
        self.click(self.SUBMIT_BUTTON)
        if self.wait_for_navigation(current_url):
            self.force_aos_visible()
        return self
 
 
    def get_office_info_text(self):
        return [item.text.strip() for item in self.find_all(self.OFFICE_INFO_ITEMS)]
 
    def is_office_info_visible(self):
        return self.is_visible(self.OFFICE_INFO_CARD)
 
    def get_phone_href(self):
        return self.find(self.PHONE_LINK).get_attribute("href")
 
    def get_whatsapp_href(self):
        return self.find(self.WHATSAPP_LINK).get_attribute("href")
 
    def get_email_href(self):
        return self.find(self.EMAIL_LINK).get_attribute("href")
 
    def is_map_present(self):
        return self.is_visible(self.MAP_IFRAME, timeout=5)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MESSAGE)
 
  
 

