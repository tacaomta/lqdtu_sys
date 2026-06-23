import json
import re

from pathlib import Path

from dashboard.models.dimensions import (
    Country,
    University,
    Author
)


# =========================================================
# LOAD UNIVERSITY KEYWORDS
# =========================================================

BASE_DIR = (

    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent

)

KEYWORD_CONFIG_PATH = (

    BASE_DIR /
    "config" /
    "university_keywords.json"

)

with open(

    KEYWORD_CONFIG_PATH,

    "r",

    encoding="utf-8"

) as f:

    UNIVERSITY_KEYWORDS = json.load(f)

# =========================================================
# PARSE AUTHORS + AFFILIATIONS
# =========================================================

def parse_authors_affiliations(text):

    """
    Parse Scopus author affiliations.

    Example:

    Author A;
    Author B;
    Author C, University X, Vietnam

    => A/B/C belong to University X
    """

    if not text:

        return []

    items = [

        x.strip()

        for x in text.split(";")

        if x.strip()

    ]

    results = []

    pending_authors = []

    for item in items:

        parts = [

            p.strip()

            for p in item.split(",")

            if p.strip()

        ]

        # =================================================
        # CASE 1
        # ONLY AUTHOR NAME
        # =================================================

        if len(parts) <= 2:

            author = ", ".join(parts)

            pending_authors.append(

                author

            )

        # =================================================
        # CASE 2
        # FULL AFFILIATION
        # =================================================

        else:

            # =============================================
            # AUTHOR
            # =============================================

            author = ", ".join(parts[:2])

            # =============================================
            # COUNTRY
            # =============================================

            country = parts[-1]

            # =============================================
            # INSTITUTION TEXT
            # =============================================

            institution_text = ", ".join(

                parts[2:-1]

            )

            # =============================================
            # CURRENT AUTHOR
            # =============================================

            results.append({

                "author": author,

                "institution_text": institution_text,

                "country": country

            })

            # =============================================
            # PENDING AUTHORS
            # =============================================

            for pa in pending_authors:

                results.append({

                    "author": pa,

                    "institution_text": institution_text,

                    "country": country

                })

            pending_authors = []

    return results

# =========================================================
# EXTRACT UNIVERSITY
# =========================================================

def extract_university(

    institution_text

):

    if institution_text is None:
        return None
    
    
    parts = [p.strip() for p in institution_text.split(',') if p.strip()]
    patterns = [
    rf"\b{re.escape(keyword)}\w*"
    for keyword in UNIVERSITY_KEYWORDS
]
    # duyệt ngược
    for p in reversed(parts):
        p_lower = p.lower()
        if any(re.search(pattern, p_lower) for pattern in patterns):
            return p
    
    return None

# =========================================================
# GET OR CREATE COUNTRY
# =========================================================

def get_or_create_country(

    country_name

):

    if not country_name:

        return None

    country_obj, _ = (

        Country.objects.get_or_create(

            name=country_name.strip()

        )

    )

    return country_obj

# =========================================================
# GET OR CREATE UNIVERSITY
# =========================================================

def get_or_create_university(

    university_name,

    country_obj=None

):

    if not university_name:

        return None

    university_obj, created = (

        University.objects.get_or_create(

            name=university_name.strip(),

            defaults={

                "country": country_obj

            }

        )

    )

    # =====================================================
    # UPDATE COUNTRY IF MISSING
    # =====================================================

    if (

        university_obj.country is None

        and country_obj is not None

    ):

        university_obj.country = country_obj

        university_obj.save()

    return university_obj


# =========================================================
# SAVE DIMENSIONS
# =========================================================

def save_dimensions(

    author_affiliations

):

    parsed_items = (

        parse_authors_affiliations(

            author_affiliations

        )

    )

    results = []
    colab_statistic = []

    for item in parsed_items:

        # ==============================================
        # COUNTRY
        # ==============================================

        country_obj = (

            get_or_create_country(

                item["country"]

            )

        )

        # ==============================================
        # UNIVERSITY
        # ==============================================

        university_name = (

            extract_university(

                item["institution_text"]

            )

        )
        colab_statistic.append({"university": university_name if university_name else "", "country": item['country']})

        university_obj = (

            get_or_create_university(

                university_name,

                country_obj

            )

        )

        # ==============================================
        # AUTHOR
        # ==============================================

        author_obj = (

            get_or_create_author(

                item["author"],

                university_obj

            )

        )

        # ==============================================
        # RESULT
        # ==============================================

        if author_obj:

            results.append({

                "author_obj": author_obj,

                "university_obj": university_obj,

                "country_obj": country_obj

            })

    return results, colab_statistic


# =========================================================
# GET OR CREATE AUTHOR
# =========================================================

def get_or_create_author(

    author_name,

    university_obj=None

):

    if not author_name:

        return None

    author_obj, _ = (

        Author.objects.get_or_create(

            name=author_name.strip(),

            university=university_obj

        )

    )

    return author_obj
