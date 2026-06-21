from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from automation.pages.login_page import LoginPage
from automation.utils import load_test_data


def test_view_leave_status():

    data = load_test_data()

    options = Options()

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    login_page = LoginPage(driver)

    login_page.open()

    login_page.login(
        data["employee_username"],
        data["employee_password"]
    )

    WebDriverWait(driver, 10).until(
        lambda d: "dashboard" in d.current_url.lower()
    )

    driver.get(
        "http://127.0.0.1:5000/leave-status"
    )

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "leaveTable")
        )
    )

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