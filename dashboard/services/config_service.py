import json

from pathlib import Path

from dashboard.models.syssetting import(
    SystemSetting
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent


# =========================================================
# LOAD JSON CONFIG
# =========================================================

def load_json_config(filename):

    config_path = (
        BASE_DIR
        / "config"
        / filename
    )

    with open(
        config_path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================================================
# REQUIRED COLUMNS
# =========================================================

def get_required_columns():

    return load_json_config(
        "required_columns.json"
    )


def set_dirty():

    SystemSetting.objects.update_or_create(

        key="config_dirty",

        defaults={

            "value": "True"

        }

    )

def clear_dirty():

    SystemSetting.objects.update_or_create(

        key="config_dirty",

        defaults={

            "value": "False"

        }

    )

def is_dirty():

    obj = SystemSetting.objects.filter(

        key="config_dirty"

    ).first()

    return (

        obj

        and

        obj.value == "True"

    )