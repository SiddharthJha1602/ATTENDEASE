from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from automation.pages.login_page import LoginPage


def test_leave_validation():

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

    submit_btn = driver.find_element(
        By.ID,
        "submitBtn"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        submit_btn
    )

    time.sleep(1)

    driver.execute_script(
        "arguments[0].click();",
        submit_btn
    )

    time.sleep(1)

    assert "apply-leave" in driver.current_url

    driver.save_screenshot(
        "automation/screenshots/leave_validation.png"
    )

    driver.quit()