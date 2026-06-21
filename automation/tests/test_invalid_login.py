from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from automation.pages.login_page import LoginPage
from automation.utils import load_test_data


def test_invalid_login():

    data = load_test_data()

    options = Options()

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    login_page = LoginPage(driver)

    login_page.open()

    login_page.login(
        data["invalid_username"],
        data["invalid_password"]
    )

    WebDriverWait(driver, 10).until(
        lambda d: "login" in d.current_url.lower()
    )

    assert "login" in driver.current_url.lower()

    driver.save_screenshot(
        "automation/screenshots/login_failed.png"
    )

    driver.quit()