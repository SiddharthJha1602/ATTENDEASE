from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from automation.utils import load_test_data
from automation.pages.login_page import LoginPage


def test_leave_validation():
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
        "http://127.0.0.1:5000/apply-leave"
    )

    WebDriverWait(driver, 10).until(
        lambda d: "apply-leave" in d.current_url.lower()
    )

    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, "submitBtn")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        submit_btn
    )

    driver.execute_script(
    "arguments[0].click();",
    submit_btn
    )

    WebDriverWait(driver, 10).until(
    EC.alert_is_present()
    )

    alert = driver.switch_to.alert

    assert "Reason must be at least 10 characters" in alert.text

    alert.accept()

    driver.save_screenshot(
        "automation/screenshots/leave_validation.png"
    )

    driver.quit()