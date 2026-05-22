import json

from pathlib import Path


# =========================================================
# BASE DIR
# =========================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)


# =========================================================
# LOAD JSON
# =========================================================

def load_json_config(

    filename

):

    path = (
        BASE_DIR /
        "config" /
        filename
    )

    with open(

        path,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)


# =========================================================
# CONFIGS
# =========================================================

LQDTU_KEYWORDS = load_json_config(
    "lqdtu_keywords.json"
)

VIETNAM_KEYWORDS = load_json_config(
    "vietnam_keywords.json"
)


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):

    if not text:

        return ""

    return (
        str(text)
        .strip()
        .lower()
    )


# =========================================================
# SPLIT AUTHOR BLOCKS
# =========================================================

def split_author_affiliations(

    authors_with_affiliations

):

    if not authors_with_affiliations:

        return []

    return [

        x.strip()

        for x in str(
            authors_with_affiliations
        ).split(";")

        if x.strip()

    ]


# =========================================================
# CHECK LQDTU
# =========================================================

def contains_lqdtu(text):

    text = normalize_text(text)

    return any(

        keyword.lower() in text

        for keyword in LQDTU_KEYWORDS

    )


# =========================================================
# CHECK VIETNAM
# =========================================================

def contains_vietnam(text):

    text = normalize_text(text)

    return any(

        keyword.lower() in text

        for keyword in VIETNAM_KEYWORDS

    )


# =========================================================
# AUTHOR COUNT
# =========================================================

def compute_author_count(

    authors

):

    if not authors:

        return 0

    author_list = [

        x.strip()

        for x in str(authors).split(";")

        if x.strip()

    ]

    return len(author_list)


# =========================================================
# IS COAUTHORED
# =========================================================

def compute_is_coauthored(

    authors

):

    return (
        compute_author_count(authors) > 1
    )


# =========================================================
# IS FIRST AUTHOR
# =========================================================

def compute_is_first_author(

    authors_with_affiliations

):

    blocks = split_author_affiliations(

        authors_with_affiliations

    )

    if not blocks:

        return False

    first_block = blocks[0]

    return contains_lqdtu(
        first_block
    )

# =========================================================
# IS CORRESPONDING
# =========================================================

def compute_is_corresponding(

    correspondence_address

):

    if not correspondence_address:

        return False

    return contains_lqdtu(
        correspondence_address
    )


# =========================================================
# IS INTERNATIONAL COLLABORATION
# =========================================================

def compute_is_international_collaboration(

    authors_with_affiliations

):

    blocks = split_author_affiliations(

        authors_with_affiliations

    )

    if not blocks:

        return False

    for block in blocks:

        if contains_vietnam(block):

            continue

        return True

    return False


# =========================================================
# IS DOMESTIC COLLABORATION
# =========================================================

def compute_is_domestic_collaboration(

    authors_with_affiliations

):

    blocks = split_author_affiliations(

        authors_with_affiliations

    )

    if not blocks:

        return False

    for block in blocks:

        is_vn = contains_vietnam(
            block
        )

        is_lqdtu = contains_lqdtu(
            block
        )

        if is_vn and not is_lqdtu:

            return True

    return False