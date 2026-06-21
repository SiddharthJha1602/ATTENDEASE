import json


def load_test_data():
    with open(
        "automation/test_data.json",
        "r"
    ) as file:
        return json.load(file)