from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from automation.pages.login_page import LoginPage


def test_valid_login():

    options = Options()

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    login_page = LoginPage(driver)

    login_page.open()

    login_page.login(
        "admin",
        "admin123"
    )

    time.sleep(3)

    print(driver.current_url)

    assert "dashboard" in driver.current_url.lower()

    driver.save_screenshot(
        "automation/screenshots/login_success.png"
    )

    driver.quit()