from django.utils import timezone

import requests

from dashboard.models.raw import (
    PublicationRaw
)


OPENALEX_URL = (
    "https://api.openalex.org/works/https://doi.org/"
)


# =========================================================
# GET FIELD FROM OPENALEX
# =========================================================

def fetch_openalex_metadata(
    doi
):

    # =====================================================
    # INVALID DOI
    # =====================================================

    if not doi:

        return {

            "field": None,

            "subfield": None,

            "openalex_id": None,

            "openalex_updated_at": None

        }

    # =====================================================
    # CLEAN DOI
    # =====================================================

    doi = (
        str(doi)
        .strip()
        .replace(
            "https://doi.org/",
            ""
        )
    )

    url = (
        OPENALEX_URL + doi
    )

    try:

        response = requests.get(

            url,

            timeout=15

        )

        if response.status_code != 200:

            return {

                "field": None,

                "subfield": None,

                 "openalex_id": None,

                 "openalex_updated_at": None

            }

        data = response.json()

        # =================================================
        # OPENALEX ID
        # =================================================

        openalex_id = data.get("id")

        # =================================================
        # PRIMARY TOPIC
        # =================================================

        primary_topic = data.get(
            "primary_topic"
        )

        if not primary_topic:

            return {

                "field": None,

                "subfield": None,

                 "openalex_id": openalex_id,

                "openalex_updated_at": None

            }

        # =================================================
        # FIELD
        # =================================================

        field_obj = primary_topic.get(
            "field"
        )

        field = (

            field_obj.get("display_name")

            if field_obj

            else None

        )

        # =================================================
        # SUBFIELD
        # =================================================

        subfield_obj = primary_topic.get(
            "subfield"
        )

        subfield = (

            subfield_obj.get("display_name")

            if subfield_obj

            else None

        )

        # =================================================
        # RETURN
        # =================================================

        return {

            

            "field": field,

            "subfield": subfield,

            "openalex_id": openalex_id,

            "openalex_updated_at": timezone.now()

        }

    except Exception:

        return {            

            "field": None,

            "subfield": None,

            "openalex_id": None,

            "openalex_updated_at": None

        }


# =========================================================
# ENRICH DATAFRAME
# =========================================================

def enrich_with_openalex(df):

    # =====================================================
    # INIT COLUMNS
    # =====================================================

    enrich_columns = [

        "openalex_id",

        "field",

        "subfield",

        "openalex_updated_at"

    ]

    for col in enrich_columns:

        if col not in df.columns:

            df[col] = None

    # =====================================================
    # PROCESS EACH ROW
    # =====================================================

    for idx, row in df.iterrows():

        doi = row.get("DOI")

        # =================================================
        # INVALID DOI
        # =================================================

        if not doi:

            continue

        doi = (
            str(doi)
            .strip()
            .lower()
            .replace(
                "https://doi.org/",
                ""
            )
        )

        # =================================================
        # CHECK EXISTING DATABASE
        # =================================================

        existing = (

            PublicationRaw.objects
            .filter(doi=doi)
            .first()

        )

        # =================================================
        # USE CACHED DATA
        # =================================================

        if existing:

            df.at[idx, "openalex_id"] = (
                existing.openalex_id
            )

            df.at[idx, "field"] = (
                existing.field
            )

            df.at[idx, "subfield"] = (
                existing.subfield
            )

            df.at[idx, "openalex_updated_at"] = (
                existing.openalex_updated_at
            )

            continue

        # =================================================
        # FETCH OPENALEX
        # =================================================

        metadata = (
            fetch_openalex_metadata(
                doi
            )
        )

        # =================================================
        # UPDATE DATAFRAME
        # =================================================

        df.at[idx, "openalex_id"] = (
            metadata.get("openalex_id")
        )

        df.at[idx, "field"] = (
            metadata.get("field")
        )

        df.at[idx, "subfield"] = (
            metadata.get("subfield")
        )

        # =================================================
        # UPDATE TIMESTAMP
        # =================================================

        if metadata.get("openalex_id"):

            df.at[idx, "openalex_updated_at"] = (
                timezone.now()
            )

    return df