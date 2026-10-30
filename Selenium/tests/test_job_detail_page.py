from pages.job_detail_page import JobDetailPage
import os

JOB_ID = 9001
CV_PATH = os.path.abspath("test_data/sample_cv.pdf")


def test_job_detail_page_loads(driver, base_url):
    """Needs job 4 ("Customer Service") in the local database."""
    page = JobDetailPage(driver).load(base_url, JOB_ID)
    assert page.is_visible(page.HERO_HEADING)
    assert page.get_title() == "QA Test Role"


def test_key_details_show_job_information(driver, base_url):
    page = JobDetailPage(driver).load(base_url, JOB_ID)
    details = page.get_key_details()
    joined = " ".join(details)
    assert "Isinya" in joined
    assert "Contract" in joined


def test_breadcrumb_links_are_displayed(driver, base_url):
    page = JobDetailPage(driver).load(base_url, JOB_ID)
    assert page.is_visible(page.BREADCRUMB_LINKS)
    assert page.get_breadcrumb_texts() == ["Home", "Careers"]


def test_required_fields_reject_empty_submit(driver, base_url):
    """The form fields are marked required, so HTML5 constraint
    validation should block submission and report the empty Email field."""
    page = JobDetailPage(driver).load(base_url, JOB_ID)
    page.submit()

    email_message = page.get_field_validation_message(page.EMAIL_INPUT)
    assert email_message != "", "Expected a validation message on empty Email field"


def test_email_field_has_max_length(driver, base_url):
    page = JobDetailPage(driver).load(base_url, JOB_ID)
    email_element = page.find(page.EMAIL_INPUT)
    assert email_element.get_attribute("maxlength") == "254"


def test_back_link_returns_to_careers_page(driver, base_url):
    page = JobDetailPage(driver).load(base_url, JOB_ID)
    page.go_back_to_vacancies()
    assert driver.current_url.rstrip("/").endswith("/careers")

def test_valid_application_shows_confirmation(driver, base_url):
    """After a valid submit, the page swaps the form for the
    .application-success-card. Unlike the contact form, the URL
    does not change (no ?sent=1), so we check the page content.
    Each run adds an application record to the local database."""
    page = JobDetailPage(driver).load(base_url, JOB_ID)
    page.fill_form(
        name="Test User",
        email="test.user@example.com",
        phone="0700000000",
        message="This is an automated test application.",
        cv_path=CV_PATH,
    )
    page.submit()

    assert page.is_visible(page.SUCCESS_MESSAGE)
    assert page.get_success_message() == "Application received!"