import pandas as pd
from dashboard.services.config_service import get_required_columns



# =========================================================
# VALIDATE REQUIRED COLUMNS
# =========================================================

def validate_required_columns(df):

    required_columns = (get_required_columns())
    
    missing_cols = [

        col
        for col in required_columns
        if col not in df.columns

    ]

    if missing_cols:

        raise ValueError(
            f"Missing required columns: {missing_cols}"
        )


# =========================================================
# SAFE INT
# =========================================================

def safe_int(value):

    if pd.isna(value):

        return None

    try:

        return int(value)

    except:

        return None


# =========================================================
# NORMALIZE DOI
# =========================================================

def normalize_doi(doi):

    if pd.isna(doi):

        return None

    doi = str(doi).strip().lower()

    if doi=="":
        return None

    return doi


# =========================================================
# REMOVE DUPLICATES
# =========================================================

def remove_duplicates(df):

    # ==========================================
    # ONLY VALID DOI
    # ==========================================

    valid_doi_mask = (

        df["DOI"].notna()

        &

        (df["DOI"].astype(str).str.strip() != "")

    )

    valid_df = df[
        valid_doi_mask
    ]

    missing_df = df[
        ~valid_doi_mask
    ]

    # ==========================================
    # DUPLICATED DOI
    # ==========================================

    duplicate_mask = df.loc[valid_doi_mask].duplicated(subset=["DOI"], keep='first')

    missing_doi_count = len(missing_df)

    duplicate_count = int(
        duplicate_mask.sum()
    )

    valid_df = valid_df[
        ~duplicate_mask
    ]

    # ==========================================
    # MERGE BACK
    # ==========================================

    final_df = pd.concat(

        [

            valid_df,

            missing_df

        ],

        ignore_index=True

    )

    return final_df, duplicate_count, missing_doi_count



# =========================================================
# PREPROCESS DATAFRAME
# =========================================================

def preprocess_dataframe(df):

    # ==========================================
    # VALIDATE COLUMNS
    # ==========================================

    validate_required_columns(df)

    # ==========================================
    # CLEAN COLUMN NAMES
    # ==========================================

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    # ==========================================
    # NORMALIZE DOI
    # ==========================================

    df["DOI"] = df["DOI"].apply(
        normalize_doi
    )

    # ==========================================
    # CLEAN YEAR
    # ==========================================

    df["Year"] = df["Year"].apply(
        safe_int
    )

    # ==========================================
    # CLEAN CITED BY
    # ==========================================

    df["Cited by"] = df["Cited by"].apply(
        safe_int
    )

    # ==========================================
    # REMOVE EMPTY TITLE
    # ==========================================

    df = df[
        df["Title"].notna()
    ]

    # ==========================================
    # REMOVE DUPLICATES
    # ==========================================

    df, duplicate_count, missing_doi_count = remove_duplicates(
        df
    )

    # ==========================================
    # RESET INDEX
    # ==========================================

    df = df.reset_index(drop=True)

    return df, duplicate_count, missing_doi_count