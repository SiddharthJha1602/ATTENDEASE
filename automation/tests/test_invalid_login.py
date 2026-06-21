from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from automation.pages.login_page import LoginPage


def test_invalid_login():

    options = Options()

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    login_page = LoginPage(driver)

    login_page.open()

    login_page.login(
        "wronguser",
        "wrongpassword"
    )

    assert "login" in driver.current_url.lower()

    driver.save_screenshot(
        "automation/screenshots/login_failed.png"
    )

    driver.quit()