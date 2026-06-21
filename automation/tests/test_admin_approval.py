from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from automation.pages.login_page import LoginPage
from automation.pages.admin_page import AdminPage
from automation.utils import load_test_data


def test_admin_approval():

    data = load_test_data()

    options = Options()

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    login_page = LoginPage(driver)

    login_page.open()

    login_page.login(
        data["admin_username"],
        data["admin_password"]
    )

    WebDriverWait(driver, 10).until(
        lambda d: "dashboard" in d.current_url.lower()
    )

    driver.get(
        "http://127.0.0.1:5000/admin/leaves"
    )

    WebDriverWait(driver, 10).until(
        lambda d: "admin/leaves" in d.current_url.lower()
    )

    admin_page = AdminPage(driver)

    result = admin_page.approve_first_pending_leave()

    assert result is True

    driver.save_screenshot(
        "automation/screenshots/admin_approval.png"
    )

    assert "admin/leaves" in driver.current_url.lower()

    driver.quit()