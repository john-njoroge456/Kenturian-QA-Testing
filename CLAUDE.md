# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Rules

- **Never edit files in `~/Kenturian-Pulp-And-Paper-Mill-Ltd`.** Use it only as a read-only reference for locators and behaviour.
- **Follow the existing Page Object Model:** define locators as class-level `(By, selector)` tuples in `pages/`. Write tests as plain functions that take `driver` and `base_url`. Reuse the `BasePage` helpers instead of calling raw Selenium waits or clicks.
- **Make one change at a time.** After each one, run `pytest -q` from `Selenium/` and show the results before committing.

## Learning mode

The repo owner is learning Selenium. For every change:

- **Concept first:** before showing code, explain the Selenium or pytest idea it relies on.
- **Line by line:** explain each line of new code — what each Selenium call does and why it was chosen over the alternatives.
- **Shared test-writing:** for each fix, write the first test yourself, then leave the next similar test for the owner to write. Describe what it should check, but don't write it.
- **Review, don't rewrite:** when the owner submits their version, review it with specific comments. Point out problems and suggest fixes, but don't replace their code with yours.
- **One question per commit:** after each commit, ask one short question that checks understanding of what was just added.

## What this repo is

QA suite for the Kenturian Pulp & Paper Mills Ltd Django website. It does not contain the application itself — the site under test lives in a separate repo (locally at `~/Kenturian-Pulp-And-Paper-Mill-Ltd`, Django app `main`). Two kinds of artifacts:

- `Selenium/` — automated UI tests (pytest + Selenium, Page Object Model).
- `KPPML_MANUAL_TESTING.xlsx` — manual test cases and regression sheets. Keep it in sync when automated expectations change (e.g. the "repair regression baseline" commit updated both).

The README mentions a `postman/` directory and lowercase `selenium/`; neither matches the repo — there is no Postman collection yet, and the directory is `Selenium/`.

## Running tests

Prerequisites: Chrome installed, and the Django site running at `http://127.0.0.1:9000` (`BASE_URL` in `Selenium/conftest.py`), e.g. from the site repo: `python manage.py runserver 9000`.

Seed the test data into the site's database first (the job detail tests depend on it):

```bash
# from ~/Kenturian-Pulp-And-Paper-Mill-Ltd
python manage.py loaddata /mnt/nvme0n1p4/Projects/Kenturian-QA-Testing/Selenium/test_data/qa_seed.json
```

Run tests **from inside `Selenium/`** — tests import `pages.*` relative to that directory and build `test_data/sample_cv.pdf` paths with `os.path.abspath`, which resolves against the CWD:

```bash
cd Selenium
source ../venv/bin/activate        # venv lives at repo root
pip install -r requirements.txt
pytest -s -v                                           # all
pytest -v tests/test_job_detail_page.py                # one file
pytest -v tests/test_job_detail_page.py::test_breadcrumb_links_are_displayed   # one test
```

There is no lint/build step.

## Architecture

- `conftest.py` provides two fixtures: `driver` (a fresh Chrome per test, quit afterward) and `base_url`.
- `pages/base_page.py` — `BasePage` holds all wait/interaction helpers (`find`, `find_clickable`, `is_visible`, `click`, `get_field_validation_message`, `wait_for_navigation`). Page objects subclass it, declare locators as class-level `(By, selector)` tuples, and expose a `load(base_url, ...)` method that navigates and returns `self` so tests can chain `Page(driver).load(base_url)`.
- `force_aos_visible()` must be called after navigation (each page's `load` does this). The site uses AOS.js scroll animations; under Selenium `[data-aos]` elements can stay at `opacity:0`, so they read as not displayed, return empty `.text`, and can intercept clicks. New page objects should call it in `load` too.
- `click()` scrolls the element into view and falls back to a JS click on `ElementClickInterceptedException`.
- Form validation is checked two ways: HTML5 constraint validation (read via `validationMessage`, since the browser blocks submit) and server-side error elements (e.g. `.form-error-note`).

## Test data conventions

- `test_data/qa_seed.json` is a Django fixture creating `main.jobposting` pk `9001` ("QA Test Role", Isinya, Contract). Job detail tests hardcode `JOB_ID = 9001` and assert on these values — change the fixture and the assertions together.
- The same fixture creates `main.newsarticle` pk `9001` ("QA Test Article", slug `qa-test-article`, published 2026-01-01, no category). News detail tests hardcode `NEWS_SLUG = "qa-test-article"`.
- Load `qa_seed.json` only into the local development database — never into the live site's database.
- Successful-submit tests write real records (applications, contact messages) into the local site database on every run; they are not cleaned up.
- Contact form success is detected by URL change (`?sent=1`); job application success is detected by the `.application-success-card` replacing the form (URL does not change).
