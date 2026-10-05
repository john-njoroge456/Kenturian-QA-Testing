import os
from pages.general_application_page import GeneralApplicationPage

CV_PATH = os.path.abspath("test_data/sample_cv.pdf")


def test_general_application_page_loads(driver, base_url):
    page = GeneralApplicationPage(driver).load(base_url)
    assert page.is_visible(page.HERO_HEADING)
    assert page.get_title() == "Send Your CV"


def test_breadcrumb_links_are_displayed(driver, base_url):
    page = GeneralApplicationPage(driver).load(base_url)
    assert page.is_visible(page.BREADCRUMB_LINKS)
    assert page.get_breadcrumb_texts() == ["Home", "Careers"]


def test_required_fields_reject_empty_submit(driver, base_url):
    """The form fields are marked required, so HTML5 constraint
    validation should block submission and report the empty Email field."""
    page = GeneralApplicationPage(driver).load(base_url)
    page.submit()

    email_message = page.get_field_validation_message(page.EMAIL_INPUT)
    assert email_message != "", "Expected a validation message on empty Email field"


def test_email_field_has_max_length(driver, base_url):
    page = GeneralApplicationPage(driver).load(base_url)
    email_element = page.find(page.EMAIL_INPUT)
    assert email_element.get_attribute("maxlength") == "320"


def test_valid_application_shows_confirmation(driver, base_url):
    """After a valid submit, the page swaps the form for the
    .application-success-card. The URL may not change, so we check
    the page content. Each run adds a record to the local database."""
    page = GeneralApplicationPage(driver).load(base_url)
    page.fill_form(
        name="Test User",
        email="test.user@example.com",
        phone="0700000000",
        message="Interested in any customer service role.",
        cv_path=CV_PATH,
    )
    page.submit()

    assert page.is_visible(page.SUCCESS_MESSAGE)
    assert page.get_success_message() == "CV received!"


def test_back_link_returns_to_careers_page(driver, base_url):
    page = GeneralApplicationPage(driver).load(base_url)
    page.go_back_to_vacancies()
    assert driver.current_url.rstrip("/").endswith("/careers")