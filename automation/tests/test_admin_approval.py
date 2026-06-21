from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from automation.pages.login_page import LoginPage
from automation.pages.admin_page import AdminPage


def test_admin_approval():

    options = Options()

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    login_page = LoginPage(driver)

    login_page.open()

    login_page.login(
        "admin",
        "admin123"
    )

    time.sleep(2)

    driver.get(
        "http://127.0.0.1:5000/admin/leaves"
    )

    time.sleep(2)

    admin_page = AdminPage(driver)

    result = admin_page.approve_first_pending_leave()

    assert result is True

    driver.save_screenshot(
        "automation/screenshots/admin_approval.png"
    )

    assert "admin/leaves" in driver.current_url.lower()

    driver.quit()