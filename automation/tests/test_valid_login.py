from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from automation.utils import load_test_data
from automation.pages.login_page import LoginPage


def test_valid_login():
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

    assert "dashboard" in driver.current_url.lower()

    driver.save_screenshot(
        "automation/screenshots/login_success.png"
    )

    driver.quit()