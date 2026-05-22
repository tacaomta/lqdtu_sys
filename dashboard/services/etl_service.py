from dashboard.models.raw import PublicationRaw
from dashboard.models.fact import FactPublication
from django.db import transaction


def transform_data():
    raws = PublicationRaw.objects.all()

    with transaction.atomic():

        for r in raws:

            if not r.doi:
                continue

            # parse authors
            authors = r.authors.split(";") if r.authors else []

            first_author_lqd = False
            if authors:
                first_author_lqd = "le quy don" in authors[0].lower()

            # citation group
            if r.cited_by == 0:
                group = "0"
            elif r.cited_by < 20:
                group = "1-19"
            else:
                group = "20+"

            # upsert
            FactPublication.objects.update_or_create(
                doi=r.doi,
                defaults={
                    "year": r.year,
                    "cited_by": r.cited_by,
                    "citation_group": group,
                    "first_author_lqd": first_author_lqd,
                }
            )