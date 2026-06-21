from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def test_empty_login():

    options = Options()

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    driver.get("http://127.0.0.1:5000")

    driver.find_element(
        "css selector",
        "button[type='submit']"
    ).click()

    assert "login" in driver.current_url.lower()

    driver.save_screenshot(
        "automation/screenshots/empty_login.png"
    )

    driver.quit()