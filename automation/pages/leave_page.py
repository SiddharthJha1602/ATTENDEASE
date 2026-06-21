from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


class LeavePage:

    def __init__(self, driver):
        self.driver = driver

    def apply_leave(
        self,
        leave_type,
        start_date,
        end_date,
        reason,
        document_path
    ):

        Select(
            self.driver.find_element(
                By.NAME,
                "leave_type"
            )
        ).select_by_visible_text(leave_type)

        self.driver.find_element(
            By.NAME,
            "start_date"
        ).send_keys(start_date)

        self.driver.find_element(
            By.NAME,
            "end_date"
        ).send_keys(end_date)

        self.driver.find_element(
            By.NAME,
            "reason"
        ).send_keys(reason)

        self.driver.find_element(
            By.NAME,
            "document"
        ).send_keys(document_path)

        submit_btn = self.driver.find_element(
            By.ID,
            "submitBtn"
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            submit_btn
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            submit_btn
        )