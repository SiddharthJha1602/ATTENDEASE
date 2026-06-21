from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from automation.pages.login_page import LoginPage


def test_view_leave_status():

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
        "http://127.0.0.1:5000/leave-status"
    )

    time.sleep(2)

    table = driver.find_element(
        By.ID,
        "leaveTable"
    )

    assert table.is_displayed()

    rows = driver.find_elements(
        By.CSS_SELECTOR,
        "#leaveBody tr"
    )

    assert len(rows) > 0

    driver.save_screenshot(
        "automation/screenshots/leave_status.png"
    )

    driver.quit()