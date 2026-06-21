from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os
from automation.utils import load_test_data
from automation.pages.login_page import LoginPage
from automation.pages.leave_page import LeavePage


def test_apply_leave():
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
        "http://127.0.0.1:5000/apply-leave"
    )

    WebDriverWait(driver, 10).until(
        lambda d: "apply-leave" in d.current_url.lower()
    )

    leave_page = LeavePage(driver)

    file_path = os.path.abspath(
        "automation/test_document.pdf"
    )

    leave_page.apply_leave(
    data["leave_type"],
    data["leave_start_date"],
    data["leave_end_date"],
    data["leave_reason"],
    file_path
    )

    WebDriverWait(driver, 10).until(
        lambda d: "leave" in d.current_url.lower()
    )

    driver.save_screenshot(
        "automation/screenshots/leave_applied.png"
    )

    assert "leave" in driver.current_url.lower()

    driver.quit()