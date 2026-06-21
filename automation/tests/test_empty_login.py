from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def test_empty_login():

    options = Options()

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    driver.get("http://127.0.0.1:5000")

    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(
            By.CSS_SELECTOR,
            "button[type='submit']"
        ).is_displayed()
    )

    driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    ).click()

    WebDriverWait(driver, 10).until(
        lambda d: "login" in d.current_url.lower()
    )

    assert "login" in driver.current_url.lower()

    driver.save_screenshot(
        "automation/screenshots/empty_login.png"
    )

    driver.quit()