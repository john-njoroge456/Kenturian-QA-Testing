from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

class BasePage:
    """Shared setup and helpers for all page objects."""

    DEFAULT_TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    from selenium.common.exceptions import TimeoutException

    def is_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
            return True
        except TimeoutException:
            return False
    
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