import json

from pathlib import Path


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
