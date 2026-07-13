# TGSRTC Bus Booking – Selenium Test Automation Framework

An end-to-end UI test automation framework built with **Python + Selenium + Pytest**, targeting the [TGSRTC](https://www.tgsrtc.telangana.gov.in/) (Telangana State Road Transport Corporation) online bus ticket booking website.

The framework automates the full ticket-booking journey — home page → route/date search → bus & seat selection → passenger details → payment confirmation — and validates the flow using data-driven test cases with automatic screenshot capture and HTML reporting.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Framework Design](#framework-design)
- [Test Coverage](#test-coverage)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Tests](#running-the-tests)
- [Test Reports](#test-reports)
- [Screenshots](#screenshots)
- [Known Limitations / Notes](#known-limitations--notes)
- [Author](#author)

---

## Overview

This project is a **Page Object Model (POM)**-based Selenium framework that drives the TGSRTC bus booking website exactly the way a real user would: searching for a route, picking a date, choosing a bus, selecting a seat, filling passenger details, and proceeding to payment. It is built to demonstrate practical, real-world web QA/SDET skills — handling dynamic pop-ups, multi-window navigation, calendar widgets, dropdown search fields, and cross-page data verification — on a **live, production website**.

The suite is data-driven: every scenario (valid booking, past date, invalid route, unavailable bus, unavailable seat, etc.) is defined once in a JSON file and executed automatically via `pytest.mark.parametrize`, so adding a new test case only requires adding a new JSON entry — no new code.

## Key Features

- **Page Object Model** with class inheritance to reuse locators and actions across the booking flow (`Base_to_Booking_page → Booking_page → Bus_and_Seat_Selection → Passenger_Details → Payments_page`)
- **Data-driven testing** — all test inputs and expected results live in `config/test_data.json`
- **Automatic screenshots** captured at key checkpoints (post-navigation, passenger details, payment page) with timestamped folders
- **Self-contained HTML reports** generated per test run via `pytest-html`, also timestamped
- **Cross-page data verification** — passenger/booking details entered in the form are re-verified against the booking summary and the final payment confirmation table, with mismatches raised as assertion errors
- **Resilient waits** — explicit `WebDriverWait` / `expected_conditions` used throughout instead of hard sleeps, with graceful handling of optional pop-ups (discount pop-up, payment pop-up)
- **Dynamic dropdown & calendar handling** — including month navigation when the target travel date falls in a future month

## Tech Stack

| Category | Tool / Library |
|---|---|
| Language | Python |
| Browser Automation | Selenium WebDriver |
| Test Runner | Pytest |
| Reporting | pytest-html |
| Data format | JSON |
| Config management | `config/config.json`, `config/test_data.json` |

See [`requirements.txt`](requirements.txt) for the full pinned dependency list.

## Project Structure

```
Travel/
├── config/
│   ├── config.json              # Environment config (base URL)
│   └── test_data.json           # Data-driven test cases (inputs + expected results)
│
├── pages/                       # Page Object Model classes
│   ├── base_to_booking_page.py  # Home page → navigate into booking flow, close pop-ups
│   ├── booking_page.py          # From/To/Date search, calendar, bus & seat count
│   ├── bus_and_seat_page.py     # Bus search, boarding/dropping point, seat selection
│   ├── passenger_details_page.py# Passenger form, gender/age/email/mobile, journey summary
│   └── payment_page.py          # Booking summary verification, payment confirmation
│
├── test/                        # Pytest test suite (one file per page/flow stage)
│   ├── test_base_to_booking_page.py
│   ├── test_booking_page.py
│   ├── test_bus_and_seat_page.py
│   ├── test_passenger_details_page.py
│   └── test_payment_page.py
│
├── reports/                      # Generated HTML test reports (timestamped)
├── screenshots/                  # Generated screenshots (timestamped folders per run)
├── conftest.py                   # Pytest fixtures: WebDriver setup/teardown, report naming
├── utilities.py                  # Helper functions: JSON loading, timestamps, screenshots
├── pytest.ini                    # Pytest configuration
└── requirements.txt              # Python dependencies
```

## Framework Design

The Page Object classes are chained through inheritance so that each stage of the booking journey has access to everything before it, without duplicating locators or driver setup:

```
Base_to_Booking_page
        │  (navigate from home page, handle discount pop-up, window switch)
        ▼
   Booking_page
        │  (From/To selection, calendar, date validation, search)
        ▼
Bus_and_Seat_Selection
        │  (bus search by service number, boarding/dropping point, seat check)
        ▼
 Passenger_Details
        │  (gender/name/age/email/mobile entry, journey summary verification)
        ▼
   Payments_page
        (booking summary vs. UI comparison, payment confirmation)
```

**Fixtures (`conftest.py`)**
- `config_load` (session-scoped) — loads `config/config.json` once per test session
- `driver` (function-scoped) — launches Chrome, navigates to the base URL, maximizes the window, yields the driver to the test, then takes a final screenshot and quits
- `pytest_configure` — dynamically names each HTML report after the test file and a run timestamp, and stores it under `reports/`

**Utilities (`utilities.py`)**
- `read_json` / `load_test_data` — loads JSON config and test data from `config/`
- `timestamp` — consistent timestamp format (`%Y_%m_%d_%H_%M_%S`) used across reports and screenshots
- `take_screenshot` — saves a screenshot into a per-run timestamped folder under `screenshots/`

## Test Coverage

Test cases are defined in `config/test_data.json` and executed as parametrized scenarios across each test file. Current scenarios include:

| Test Case | Scenario | Expected Outcome |
|---|---|---|
| Test_000 | Past date selected | "Past Date is selected" |
| Test_001 | Journey date more than 2 months in the future | "No Buses available for the Day!" |
| Test_002 | Route with no bus service (Hyderabad → Achampet) | "No Buses available for the Day!" |
| Test_003 | Valid route/date, invalid bus service number | "Service number is unavailable" |
| Test_004 | Valid bus, already-booked/unavailable seat | "Seat is unavailable for booking" |
| Test_005 | Fully valid booking (route, date, bus, seat, passenger details) | Booking proceeds to payment |
| Test_006 | Seat currently on hold | "Seat is currently unavailable for booking" |

Each test file (`test_base_to_booking_page.py` → `test_payment_page.py`) automates progressively deeper into the booking flow, reusing the same data set, so the suite effectively tests the flow at increasing levels of depth (smoke → booking search → seat selection → passenger form → full payment flow).

## Prerequisites

- Python 3.10+ installed
- Google Chrome installed (the framework uses `webdriver.Chrome()` with Selenium's built-in driver management)
- Internet access, since tests run against the live TGSRTC website

## Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Travel

# 2. (Recommended) Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

## Configuration

Update `config/config.json` if the target environment changes:

```json
{
    "base_url": "https://www.tgsrtc.telangana.gov.in/"
}
```

Update `config/test_data.json` to add or modify test scenarios. Each entry supports the following keys (only the ones relevant to that scenario need to be present):

```json
{
  "test_case_id": "Test_005 Valid Date and Route",
  "from_loc": "HYDERABAD",
  "to_loc": "TIRUPATI",
  "date_of_journey": "2026-03-20",
  "bus_ser_no": "1453",
  "boarding_pt": "MGBS",
  "dropping_pt": "TIRUPATI BS",
  "seat_no": "18",
  "pass_gender": "Male",
  "pass_name": "Ttt",
  "pass_age": "24",
  "pass_email": "Ttt@gmail.com",
  "pass_mobile": "9012345678",
  "error_or_message": "Seat is available and Payment Processed"
}
```

> **Note:** `date_of_journey` values must be kept current relative to the day the suite is run — dates too far in the past/future will intentionally trigger the "past date" / "no buses available" scenarios.

## Running the Tests

Run the full suite:

```bash
pytest
```

Run a specific test file:

```bash
pytest test/test_payment_page.py
```

Run a specific scenario by its test ID:

```bash
pytest test/test_booking_page.py -k "Test_005"
```

Pytest options are pre-configured in `pytest.ini`:

```ini
[pytest]
addopts = -v -s --self-contained-html
testpaths = test
python_files = test_*.py
```

This means every run automatically produces a verbose console log and a self-contained HTML report — no extra flags needed.

## Test Reports

Every run generates a timestamped, self-contained HTML report under `reports/`, e.g.:

```
reports/test_payment_page_2026_03_02_20_51_35.html
```

The report name is derived automatically from the test file and run timestamp (see `pytest_configure` in `conftest.py`), so historical runs are never overwritten.

## Screenshots

Screenshots are captured automatically at key points in the flow (end of each test, passenger details step, payment/QR step) and saved into a timestamped folder per run:

```
screenshots/2026_03_02_20_51_35/
├── Page_Upto_Processed.png
├── Passenger_Details.png
└── Payment_Page.png
```

## Known Limitations / Notes

- Tests run against the **live production website** — there is no mock/staging environment, so test data (routes, bus service numbers, seat numbers) must reflect currently available services and may need periodic updates.
- Browser execution is currently local (Chrome only); no headless or CI/CD pipeline configuration is included in this project yet.
- `date_of_journey` values in `test_data.json` are static and will need to be refreshed periodically to stay valid relative to "today."
- No `.gitignore` is currently included — recommended to exclude `screenshots/`, `reports/`, `__pycache__/`, and `.pytest_cache/` from version control.

## Author

**Thulasi Reddy Varakantham**
SDET / Software Test Engineer — transitioning from automotive embedded (MIL/SIL) testing into IT/SaaS QA and SDET roles.
Built as a hands-on portfolio project to demonstrate Selenium, Python, Pytest, and Page Object Model skills on a real, live web application.
