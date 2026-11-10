from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

class BasePage:
    """Shared setup and helpers for all page objects."""

    DEFAULT_TIMEOUT = 10

    NAV_MENU = (By.ID, "navMain")
    NAV_ACTIVE_LINKS = (By.CSS_SELECTOR, "#navMain .nav-link.active")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def is_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
            return True
        except TimeoutException:
            return False

    def is_hidden(self, locator, timeout=3):
        """Waits for the element to become hidden (or be removed).
        is_visible can't answer this: it waits for the element to appear."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def type_into(self, locator, text):
        """Types without clearing first, so the field fires an input event
        the way a user editing it would."""
        self.find(locator).send_keys(text)

    def has_invalid_class(self, locator):
        classes = self.find(locator).get_attribute("class") or ""
        return "is-invalid" in classes.split()

    def get_field_errors(self, locator):
        """Texts of the server-side .field-error divs that follow the input.
        Read immediately with no wait, so an empty list means none are there."""
        element = self.find(locator)
        errors = element.find_elements(
            By.XPATH, "following-sibling::div[contains(concat(' ', normalize-space(@class), ' '), ' field-error ')]"
        )
        return [el.text.strip() for el in errors]

    def get_active_nav_texts(self):
        """Texts of the highlighted main-nav links. Read without waiting
        once the nav exists, so an empty list means none is active."""
        self.find(self.NAV_MENU)
        links = self.driver.find_elements(*self.NAV_ACTIVE_LINKS)
        return [el.text.strip() for el in links]

    def get_text(self, locator):

        return self.find(locator).text.strip()

    def click(self, locator):
        element = self.find_clickable(locator)
        self.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center',behavior: 'smooth'});", element
    )
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
   
    def force_aos_visible(self):
        """AOS.js only marks an element as animated-in once its own
    scroll-into-view check fires. Under Selenium that check
    doesn't always trigger the way it does for a real user
    scrolling, so [data-aos] elements can get stuck at
    opacity:0 — which Selenium reports as not displayed, with
    empty .text, and can even block clicks on whatever sits
    underneath. This forces every AOS element straight to the
    state it would eventually reach on its own, so tests act on
    fully-rendered content instead of racing the animation."""
        self.driver.execute_script(
            "document.querySelectorAll('[data-aos]').forEach(el => {"
            "el.style.transition = 'none';"
            "el.classList.add('aos-animate');"
            "});"
        )


    
    def get_field_validation_message(self, locator):
        """Reads the browser's built-in HTML5 validation message
                (e.g. 'Please fill out this field') for a required input
                that failed constraint validation on submit.
                """
        element = self.find(locator)
        return self.driver.execute_script( 
            "return arguments[0].validationMessage;", element ) 

    def wait_for_navigation(self, from_url, timeout=3):
     try:
        WebDriverWait(self.driver, timeout).until(EC.url_changes(from_url))
        return True
     except TimeoutException:
        return False