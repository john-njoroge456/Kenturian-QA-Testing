# Kenturian QA Testing

Automated and manual QA testing for the Kenturian Pulp & Paper Mills Ltd website (Django), covering UI testing with Selenium/pytest and API testing with Postman.

## Structure

```
Kenturian-QA-Testing/
├── selenium/
│   ├── conftest.py
│   ├── requirements.txt
│   ├── pages/          # Page Object Model classes
│   └── tests/          # pytest test files
├── postman/
│   ├── Kenturian.postman_collection.json
│   └── Kenturian.postman_environment.json
└── README.md
```

## Prerequisites

- Python 3.10+
- Google Chrome installed
- The Kenturian Django site running locally (`python manage.py runserver 9000` or equivalent), since these tests target `http://127.0.0.1:9000/`

## Setup — Selenium tests

```bash
cd selenium
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the tests

```bash
pytest -s -v
```

## Setup — Postman/API tests

Import `postman/Kenturian.postman_collection.json` and `postman/Kenturian.postman_environment.json` into Postman, or run via Newman:

```bash
newman run postman/Kenturian.postman_collection.json -e postman/Kenturian.postman_environment.json
```

## Notes

- These are automated tests. A separate manual test plan and test case document (`Kenturian_Test_Plan.md` / `Kenturian_Test_Cases.xlsx`) covers exploratory and manual test coverage for the site.
- Test coverage is being built incrementally, starting with the Contact form.
