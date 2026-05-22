import json
from pathlib import Path

from django.conf import settings
from django.utils import timezone


CONFIG_PATH = (
    Path(settings.BASE_DIR)
    / "config"
    / "citation_groups.json"
)


def load_citation_config():

    """
    Load citation grouping config
    """

    with open(
        CONFIG_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def compute_citation_group(cited_by):

    """
    Tính citation group từ config
    """

    if cited_by is None:
        return "Unknown"

    groups = load_citation_config()

    for group in groups:

        min_value = group["min"]
        max_value = group["max"]

        if max_value is None:

            if cited_by >= min_value:
                return group["code"]

        else:

            if min_value <= cited_by <= max_value:
                return group["code"]

    return "Unknown"


def update_citation_group(publication):

    """
    Update citation group cho publication
    """

    publication.citation_group = (
        compute_citation_group(
            publication.cited_by
        )
    )

    publication.citation_updated_at = (
        timezone.now()
    )

    publication.save(
        update_fields=[
            "citation_group",
            "citation_updated_at",
        ]
    )


def bulk_update_citation_groups(queryset):

    """
    Bulk update citation groups
    """

    now = timezone.now()

    updated_objects = []

    for publication in queryset:

        publication.citation_group = (
            compute_citation_group(
                publication.cited_by
            )
        )

        publication.citation_updated_at = now

        updated_objects.append(publication)

    if updated_objects:

        model = type(updated_objects[0])

        model.objects.bulk_update(
            updated_objects,
            [
                "citation_group",
                "citation_updated_at"
            ],
            batch_size=500
        )

    return len(updated_objects)

def get_citation_groups():

    """
    Return groups cho UI
    """

    groups = load_citation_config()

    return [
        (g["code"], g["label"])
        for g in groups
    ]

