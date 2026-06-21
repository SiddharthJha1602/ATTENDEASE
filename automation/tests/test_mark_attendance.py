from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from automation.pages.login_page import LoginPage
from automation.pages.attendance_page import AttendancePage


def test_mark_attendance():

    options = Options()

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    login_page = LoginPage(driver)

    login_page.open()

    # Use EMPLOYEE credentials
    login_page.login(
        "siddharth",
        "siddharth123"
    )

    time.sleep(2)

    driver.get("http://127.0.0.1:5000/attendance")

    time.sleep(2)

    attendance = AttendancePage(driver)

    attendance.mark_attendance()

    time.sleep(2)

    assert "attendance" in driver.current_url.lower()

    driver.save_screenshot(
        "automation/screenshots/attendance_marked.png"
    )

    driver.quit()