import os
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver", None)

        if driver:
            os.makedirs(
                "automation/screenshots/failures",
                exist_ok=True
            )

            file_name = (
                f"automation/screenshots/failures/"
                f"{item.name}.png"
            )

            driver.save_screenshot(file_name)