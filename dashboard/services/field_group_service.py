import json
import pandas as pd

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


# =========================================================
# LOAD CONFIG
# =========================================================

def load_field_group_config():

    path = (
        BASE_DIR /
        "config" /
        "field_groups.json"
    )

    with open(

        path,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)


FIELD_GROUP_CONFIG = (
    load_field_group_config()
)


# =========================================================
# COMPUTE FIELD GROUP
# =========================================================

def compute_field_group(
    field,
    subfield=None
):

    # =====================================================
    # SUPPORT PANDAS APPLY(row)
    # =====================================================

    if isinstance(field, pd.Series):

        row = field

        field = row.get("field")

        subfield = row.get("subfield")

    # =====================================================
    # NULL FIELD
    # =====================================================

    if pd.isna(field) or not field:

        return "Others"

    # =====================================================
    # LOOP CONFIG
    # =====================================================

    for group_name, config in (

        FIELD_GROUP_CONFIG.items()

    ):

        fields = config.get(
            "fields",
            []
        )

        subfields = config.get(
            "subfields",
            []
        )

        # =================================================
        # FIELD MATCH
        # =================================================

        if field in fields:

            # =============================================
            # SUBFIELD RULE
            # =============================================

            if subfields:

                if subfield in subfields:

                    return group_name

            else:

                return group_name

    # =====================================================
    # FALLBACK
    # =====================================================

    if field == "Engineering":

        return (
            "Engineering and Technology"
        )

    return "Others"


# =========================================================
# GET FIELD GROUPS
# =========================================================

def get_field_groups():

    return list(

        FIELD_GROUP_CONFIG.keys()

    )