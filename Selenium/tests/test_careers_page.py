from pages.careers_page import CareersPage


def test_careers_page_loads(driver, base_url):
    page = CareersPage(driver).load(base_url)
    assert page.get_hero_heading() == "Careers"


def test_job_cards_are_displayed(driver, base_url):
    """Needs at least one job in the local database. Every card
    should show a non-empty title."""
    page = CareersPage(driver).load(base_url)
    assert page.get_job_card_count() >= 1
    titles = page.get_job_titles()
    assert "" not in titles


def test_view_and_apply_opens_job_detail(driver, base_url):
    page = CareersPage(driver).load(base_url)
    page.open_job(0)
    assert driver.current_url.rstrip("/").split("/")[-1].isdigit()


def test_employee_stories_section_is_visible(driver, base_url):
    page = CareersPage(driver).load(base_url)
    assert page.is_stories_section_visible()


def test_employee_stories_has_five_slots(driver, base_url):
    """The template always renders five slots; the JavaScript fills
    them with the real stories, so this holds whatever the story count."""
    page = CareersPage(driver).load(base_url)
    assert page.get_story_slot_count() == 5


def test_active_story_shows_author(driver, base_url):
    """Needs at least one employee story in the database. With none,
    the page script exits early and the author name stays empty."""
    page = CareersPage(driver).load(base_url)
    assert page.get_story_author_name() != ""


def test_cta_opens_general_application_page(driver, base_url):
    page = CareersPage(driver).load(base_url)
    page.open_general_application()
    assert page.is_visible(page.HERO_HEADING)
    assert page.get_hero_heading() == "Send Your CV"