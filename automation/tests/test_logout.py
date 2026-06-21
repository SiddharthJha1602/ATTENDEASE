from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from automation.pages.login_page import LoginPage


def test_logout():

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

    driver.find_element(
        By.CLASS_NAME,
        "nav-logout"
    ).click()

    time.sleep(2)

    assert "login" in driver.current_url.lower()

    driver.save_screenshot(
        "automation/screenshots/logout_success.png"
    )

    driver.quit()