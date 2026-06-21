from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from automation.pages.login_page import LoginPage
from automation.utils import load_test_data


def test_logout():

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

    logout_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "nav-logout")
        )
    )

    logout_btn.click()

    WebDriverWait(driver, 10).until(
        lambda d: "login" in d.current_url.lower()
    )

    assert "login" in driver.current_url.lower()

    driver.save_screenshot(
        "automation/screenshots/logout_success.png"
    )

    driver.quit()