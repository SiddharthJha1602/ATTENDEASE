# ATTENDEASE – HR Management System with Selenium Automation Testing

## Overview

ATTENDEASE is a Human Resource Management System (HRMS) developed using Python and Flask. The project includes a complete Selenium-based automation testing framework built with PyTest and the Page Object Model (POM) design pattern.

The automation suite validates critical business workflows including authentication, attendance management, leave management, and administrative approvals.

---

## Features

### Employee Features

* Employee Login
* Attendance Management
* Attendance Export
* Leave Application
* Leave Status Tracking

### Admin Features

* Leave Request Review
* Leave Approval Management

### Automation Framework Features

* Selenium WebDriver Automation
* Page Object Model (POM)
* Explicit Waits using WebDriverWait
* Assertions for All Test Cases
* Externalized Test Data using JSON
* Screenshot Capture for Test Scenarios
* HTML Execution Reports using pytest-html

---

## Technology Stack

| Component         | Technology              |
| ----------------- | ----------------------- |
| Backend           | Python, Flask           |
| Frontend          | HTML, CSS, JavaScript   |
| Database          | SQLite                  |
| Automation        | Selenium WebDriver      |
| Testing Framework | PyTest                  |
| Design Pattern    | Page Object Model (POM) |
| Reporting         | pytest-html             |
| Version Control   | Git & GitHub            |
| Deployment        | Render                  |

---

## Automated Test Cases

### Authentication Tests

* Valid Login
* Invalid Login
* Empty Login Validation
* Logout Functionality

### Attendance Tests

* Mark Attendance
* Duplicate Attendance Validation

### Leave Management Tests

* Apply Leave Successfully
* Leave Form Validation
* View Leave Status

### Administrative Tests

* Admin Leave Approval

---

## Project Structure

```text
ATTENDEASE
│
├── automation
│   ├── pages
│   ├── tests
│   ├── screenshots
│   ├── reports
│   ├── test_data.json
│   └── conftest.py
│
├── templates
├── static
├── uploads
│
├── app.py
├── requirements.txt
├── README.md
└── report.html
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd ATTENDEASE
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running Automated Tests

Execute all test cases:

```bash
pytest automation/tests -v
```

Generate an HTML report:

```bash
pytest automation/tests -v --html=automation/reports/report.html
```

---

## Test Artifacts

The automation framework generates:

* HTML Execution Reports
* Test Screenshots
* Validation Logs
* Detailed Test Results

Report Location:

```text
automation/reports/report.html
```

Screenshots Location:

```text
automation/screenshots/
```

---

## Results

✅ All automated test cases executed successfully

✅ Selenium WebDriver automation implemented

✅ Page Object Model (POM) architecture used

✅ Explicit waits implemented using WebDriverWait

✅ Test data externalized using JSON

✅ HTML execution report generated

✅ Attendance, Leave, Login, Logout, and Admin workflows automated

---

## Author

**Siddharth Jha**

B.Tech Computer Science Engineering
Manipal University Jaipur
