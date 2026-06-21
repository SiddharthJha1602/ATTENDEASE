from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

from automation.pages.login_page import LoginPage
from automation.pages.leave_page import LeavePage


def test_apply_leave():

    options = Options()

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    login_page = LoginPage(driver)

    login_page.open()

    login_page.login(
        "siddharth",
        "siddharth123"
    )

    time.sleep(2)

    driver.get(
    "http://127.0.0.1:5000/apply-leave"
    )

    time.sleep(2)

    leave_page = LeavePage(driver)

    file_path = os.path.abspath(
        "automation/test_document.pdf"
    )

    leave_page.apply_leave(
    "Casual Leave",
    "2026-06-25",
    "2026-06-26",
    "Family function leave request",
    file_path
    )

    time.sleep(3)

    driver.save_screenshot(
        "automation/screenshots/leave_applied.png"
    )

    assert "leave" in driver.current_url.lower()

    driver.quit()