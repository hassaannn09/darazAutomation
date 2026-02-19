<div align="center">

# Daraz Automation Testing Project

**Automated end-to-end product search, filtering, and reporting for Daraz.pk**  
Built with Python · Selenium · Page Object Model · Live HTML Dashboard

[![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)](https://python.org)
[![Selenium](https://img.shields.io/badge/-Selenium-43B02A?logo=selenium&logoColor=white)](https://selenium.dev)
[![ChromeDriver](https://img.shields.io/badge/-ChromeDriver-4285F4?logo=googlechrome&logoColor=white)](https://chromedriver.chromium.org)
[![Status](https://img.shields.io/badge/-Passing-22c55e?logo=checkmarx&logoColor=white)](.)

</div>

---

## Overview

This project automates real user interactions on [Daraz.pk](https://www.daraz.pk) using Selenium WebDriver and Python. After each test run, it generates a `report.json` and automatically launches a **live one-page HTML dashboard** to visualize results.

---

## What The Test Does

<div>

| Step | Action | Detail |
|------|--------|--------|
| 1 | Open Browser | Chrome launches and maximizes |
| 2 | Navigate | Opens `https://www.daraz.pk` |
| 3 | Search | Searches for `"electronics"` |
| 4 | Brand Filter | Filters by **Planet X** |
| 5 | Price Filter | Sets range **PKR 500 – 5,000** |
| 6 | Count Products | Asserts `product_count > 0` |
| 7 | Open Product | Clicks the first result |
| 8 | Free Shipping | Checks for Free Shipping label |
| 9 | Report | Saves `report.json`, opens dashboard |

</div>

---

## Tech Stack

<div>

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Automation | Selenium WebDriver |
| Architecture | Page Object Model (POM) |
| Report Format | JSON |
| Dashboard | HTML · CSS · JavaScript |
| Server | Python `http.server` |

</div>

---

## Project Structure

```
darazAutomation/
│
├── drivers/
│   └── chromedriver.exe
│
├── pages/
│   ├── __init__.py
│   ├── base_page.py        ← Shared Selenium helpers
│   ├── home_page.py        ← Search functionality
│   ├── search_page.py      ← Filters & product listing
│   └── product_page.py     ← Product detail checks
│
├── test_daraz.py           ← Main test runner
├── dashboard.html          ← Live result dashboard
├── report.json             ← Auto-generated after test
└── README.md
```

---

## Setup

### 1. Install Dependencies

```bash
pip install selenium
```

###  2. ChromeDriver

Download the ChromeDriver version matching your Chrome browser from:  
https://chromedriver.chromium.org/downloads

Place `chromedriver.exe` inside the `drivers/` folder.

---

## Run The Test

```bash
python test_daraz.py
```

After the test completes:
- `report.json` is saved automatically
- A local server starts on port `8000`
- Dashboard opens at **http://localhost:8000/dashboard.html**

> No manual steps needed — everything is automatic.

---

## Sample Report (`report.json`)

```json
{
  "test_name": "Daraz Automation Test",
  "search_term": "electronics",
  "brand": "Planet X",
  "price_range": "500-5000",
  "product_count": 12,
  "free_shipping": true,
  "status": "PASS",
  "execution_time_seconds": 18.4
}
```

---

## Test Result Logic

<div>

| Condition | Result |
|-----------|--------|
| Products found > 0 | PASS |
| No products found | FAIL |
| Exception occurred | FAIL |

</div>

---

## Features

<div>

- **Page Object Model (POM)** — clean, maintainable structure
- **Dynamic JSON report** — generated on every run
- **Live HTML dashboard** — auto-opens after test
- **Error handling** — graceful failure with status tracking
- **Auto port cleanup** — no "port in use" errors on re-runs
- **Internship-ready** — professional code structure

</div>

---

## Future Improvements

-  Screenshot capture on failure
- File-based logging
- PyTest framework migration
-  Headless mode support
- CI/CD integration (GitHub Actions)
- Test history & trend tracking
- PDF report export

---

## Author

<div>

**Muhammad Hassaan** <br> QA Intern - 10Pearls <br>

</div>

---
<div align="center">

This project is for **educational and demonstration purposes** only.
</div>
