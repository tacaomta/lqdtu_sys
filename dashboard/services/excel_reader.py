import pandas as pd


def read_publication_file(file):

    filename = file.name.lower()

    # =====================================================
    # EXCEL
    # =====================================================

    if filename.endswith(".xlsx"):

        return pd.read_excel(file)

    if filename.endswith(".xls"):

        return pd.read_excel(file)

    # =====================================================
    # CSV
    # =====================================================

    if filename.endswith(".csv"):

        return pd.read_csv(file)

    # =====================================================
    # INVALID
    # =====================================================

    raise ValueError(
        "Unsupported file format"
    )