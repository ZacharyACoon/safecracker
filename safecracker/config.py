import json


def get_relative_config_json():
    with open("config.json") as f:
        return json.load(f)
