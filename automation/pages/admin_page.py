from selenium.webdriver.common.by import By
import time


class AdminPage:

    def __init__(self, driver):
        self.driver = driver

    def approve_first_pending_leave(self):

        approve_buttons = self.driver.find_elements(
            By.CLASS_NAME,
            "btn-approve"
        )

        if len(approve_buttons) > 0:

            approve_buttons[0].click()

            time.sleep(1)

            alert = self.driver.switch_to.alert

            alert.accept()

            time.sleep(2)

            return True

        return False