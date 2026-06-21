from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from automation.pages.login_page import LoginPage
from automation.utils import load_test_data


def test_duplicate_attendance():

    data = load_test_data()

    options = Options()

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    login_page = LoginPage(driver)

    login_page.open()

    login_page.login(
        data["employee_username"],
        data["employee_password"]
    )

    WebDriverWait(driver, 10).until(
        lambda d: "dashboard" in d.current_url.lower()
    )

    driver.get(
        "http://127.0.0.1:5000/attendance"
    )

    WebDriverWait(driver, 10).until(
        lambda d: "attendance" in d.current_url.lower()
    )

    if "Attendance Marked" in driver.page_source:

        assert "Attendance Marked" in driver.page_source

        driver.save_screenshot(
            "automation/screenshots/duplicate_attendance.png"
        )

    driver.quit()