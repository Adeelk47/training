import json
import logging
import os
from pathlib import Path


class Settings:
    local_settings = None

    def __getattr__(cls, key):
        if key in cls.local_settings:
            return cls.local_settings[key]


settings = None
if not settings:
    settings = Settings()
    project_root = str(Path(__file__).parent.parent.parent)
    try:
        with open(os.path.join(project_root, "etc", "settings.json"), "r") as file:
            configs = json.load(file)
            if "ENVIRONMENT" not in configs or configs["ENVIRONMENT"] not in configs:
                raise Exception("Unexpected settings file format, bad ENV")
            settings.local_settings = configs[configs["ENVIRONMENT"]]
    except FileNotFoundError:
        logging.error("Please add settings.local.json file in etc")
        raise
    except json.decoder.JSONDecodeError:
        logging.error("settings.local.json file not in a readable json format")
        raise
