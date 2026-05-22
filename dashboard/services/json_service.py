import math
import numpy as np
import pandas as pd

from datetime import datetime


# =========================================================
# SANITIZE JSON
# =========================================================

def sanitize_json(data):

    # =====================================================
    # NONE
    # =====================================================

    if data is None:

        return None

    # =====================================================
    # DICT
    # =====================================================

    if isinstance(data, dict):

        return {

            str(k): sanitize_json(v)

            for k, v in data.items()

        }

    # =====================================================
    # LIST
    # =====================================================

    if isinstance(data, list):

        return [

            sanitize_json(v)

            for v in data

        ]

    # =====================================================
    # DATETIME
    # =====================================================

    if isinstance(data, datetime):

        return data.isoformat()

    # =====================================================
    # PANDAS TIMESTAMP
    # =====================================================

    if isinstance(data, pd.Timestamp):

        return data.isoformat()

    # =====================================================
    # NUMPY INTEGER
    # =====================================================

    if isinstance(data, np.integer):

        return int(data)

    # =====================================================
    # NUMPY FLOAT
    # =====================================================

    if isinstance(data, np.floating):

        value = float(data)

        if math.isnan(value):

            return None

        return value

    # =====================================================
    # NUMPY BOOL
    # =====================================================

    if isinstance(data, np.bool_):

        return bool(data)

    # =====================================================
    # NaN
    # =====================================================

    if pd.isna(data):

        return None

    # =====================================================
    # DEFAULT
    # =====================================================

    return data
