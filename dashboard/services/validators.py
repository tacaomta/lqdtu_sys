import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def load_required_columns():

    path = (
        BASE_DIR /
        "config" /
        "required_columns.json"
    )

    with open(path, "r", encoding="utf-8") as f:

        return json.load(f)


def validate_required_columns(df):

    required_columns = load_required_columns()

    missing = []

    for col in required_columns:

        if col not in df.columns:

            missing.append(col)

    if missing:

        raise ValueError(
            f"Missing required columns: {missing}"
        )
