from pages.contact_page import ContactPage

def test_contact_page_loads(driver, base_url):
    page = ContactPage(driver)
    page.load(base_url)
    assert "Contact" in driver.title
    assert page.find(page.NAME_INPUT).is_displayed()

def test_required_fields_reject_empty_submit(driver, base_url):
    """All four fields are marked required with no server round-trip
    needed to catch this — HTML5 constraint validation should block
    submission and report each empty field."""
    page = ContactPage(driver).load(base_url)
    page.submit()

    name_message = page.get_field_validation_message(page.NAME_INPUT)
    assert name_message != "", "Expected a validation message on empty Name field"

def test_message_field_has_no_max_length(driver, base_url):
    """Documents a known bug: unlike Name/Email/Subject, the Message
    textarea has no maxlength attribute, so it accepts unbounded input."""
    page = ContactPage(driver).load(base_url)
    message_element = page.find(page.MESSAGE_TEXTAREA)
    assert message_element.get_attribute("maxlength") is None

def test_office_info_panel_displays_contact_details(driver, base_url):
    page = ContactPage(driver).load(base_url)
    info_text = page.get_office_info_text()
    joined = " ".join(info_text)
    assert "Kajiado" in joined
    assert "kenturianpaper@gmail.com" in joined

def test_office_info_panel_is_visible(driver, base_url):
    page = ContactPage(driver).load(base_url)
    assert page.is_office_info_visible()

def test_contact_links_point_to_correct_targets(driver, base_url):
    page = ContactPage(driver).load(base_url)
    assert page.get_phone_href() == "tel:+254720044513"
    assert page.get_whatsapp_href() == "https://wa.me/254795979982"
    assert page.get_email_href() == "mailto:kenturianpaper@gmail.com"

def test_map_is_present(driver, base_url):
    page = ContactPage(driver).load(base_url)
    assert page.is_map_present()

def test_successful_submission_shows_confirmation(driver, base_url):
    """After a valid submit, the Django view redirects with a
    ?sent=1 query param and the template swaps the form out for
    an .application-success-card (see contact.html's {% if sent %}
    block) — there is no visible way back to a blank form, which
    matches the Medium-severity bug already logged manually."""
    page = ContactPage(driver).load(base_url)
    page.fill_form(
        name="Test User",
        email="test.user@example.com",
        subject="QA test message",
        message="This is an automated test submission.",
    )
    page.submit()

    assert "sent=1" in driver.current_url
    assert page.get_success_message() == "Message Sent!"