# ATTENDEASE

 Management System with Selenium Automation Testing.

## Features

- Employee Login
- Attendance Management
- Leave Application
- Leave Status Tracking
- Admin Leave Approval
- Attendance Export

## Automation Framework

Technology Stack:

- Python
- Selenium WebDriver
- PyTest
- Page Object Model (POM)

## Automated Test Cases

1. Valid Login
2. Invalid Login
3. Empty Login
4. Logout
5. Mark Attendance
6. Duplicate Attendance
7. Apply Leave Successfully
8. Leave Form Validation
9. View Leave Status
10. Admin Approval

## Test Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run all tests:

```bash
pytest automation/tests -v
```

Generate HTML Report:

```bash
pytest automation/tests -v --html=automation/reports/report.html
```

## Project Structure

```text
ATTENDEASE
│
├── automation
│   ├── pages
│   ├── tests
│   ├── screenshots
│   └── reports
│
├── templates
├── static
├── app.py
├── requirements.txt
└── README.md
```

## Result

All automated test cases passed successfully using Selenium WebDriver and PyTest.
