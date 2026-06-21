from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminPage:

    def __init__(self, driver):
        self.driver = driver

    def approve_first_pending_leave(self):

        approve_buttons = self.driver.find_elements(
            By.CLASS_NAME,
            "btn-approve"
        )

        if len(approve_buttons) > 0:

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                approve_buttons[0]
            )

            self.driver.execute_script(
                "arguments[0].click();",
                approve_buttons[0]
            )

            WebDriverWait(self.driver, 10).until(
                EC.alert_is_present()
            )

            alert = self.driver.switch_to.alert

            alert.accept()

            return True

        return False