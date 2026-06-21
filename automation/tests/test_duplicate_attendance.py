from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from automation.pages.login_page import LoginPage


def test_duplicate_attendance():

    options = Options()

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    login_page = LoginPage(driver)

    login_page.open()

    # Employee account
    login_page.login(
        "siddharth",
        "siddharth123"
    )

    time.sleep(2)

    driver.get(
        "http://127.0.0.1:5000/attendance"
    )

    time.sleep(2)

    # Try marking attendance again
    if "Attendance Marked" in driver.page_source:

        assert "Attendance Marked" in driver.page_source

        driver.save_screenshot(
            "automation/screenshots/duplicate_attendance.png"
        )

    driver.quit()