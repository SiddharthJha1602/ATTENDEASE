from selenium.webdriver.common.by import By


class AttendancePage:

    def __init__(self, driver):
        self.driver = driver

    def mark_attendance(self):

        buttons = self.driver.find_elements(
            By.CLASS_NAME,
            "btn-mark-att"
        )

        if buttons:
            buttons[0].click()