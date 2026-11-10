from pages.news_detail_page import NewsDetailPage

NEWS_SLUG = "qa-test-article"


def test_news_detail_page_loads(driver, base_url):
    """Needs news article 9001 from qa_seed.json in the local database."""
    page = NewsDetailPage(driver).load(base_url, NEWS_SLUG)
    assert page.is_visible(page.HERO_HEADING)
    assert page.get_title() == "QA Test Article"


def test_news_nav_link_is_active(driver, base_url):
    """FX-21: the News nav link stays highlighted on an article page."""
    page = NewsDetailPage(driver).load(base_url, NEWS_SLUG)
    assert page.get_active_nav_texts() == ["News"]
