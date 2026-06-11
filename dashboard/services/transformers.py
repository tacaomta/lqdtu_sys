from django.db import transaction
from django.utils import timezone

from dashboard.models import (
    PublicationRaw,
    FactPublication
)

from dashboard.services.cleaners import clean_authors

from dashboard.models.dimensions import (

    Author,

    University,

    Country

)

from dashboard.services.field_group_service import (
    compute_field_group
)

from dashboard.services.citation_service import (
    compute_citation_group
)

from dashboard.services.collaboration_service import (

    compute_author_count,

    compute_is_coauthored,

    compute_is_first_author,

    compute_is_corresponding,

    compute_is_international_collaboration,

    compute_is_domestic_collaboration

)

from dashboard.models.bridges import (
     PublicationAuthor 
)

from dashboard.services.dimension_service import (
    save_dimensions
)



# =========================================================
# TRANSFORM PUBLICATIONS
# =========================================================

def transform_publications(

    batch_size=500,

    force_rebuild=False

):

    """
    Transform RAW publications
    into FactPublication.
    """

    # =====================================================
    # QUERYSET
    # =====================================================

    queryset = (
        PublicationRaw.objects.all()
    )

    if not force_rebuild:

        queryset = queryset.filter(
            processed=False
        )

    raw_rows = list(queryset)

    # =====================================================
    # EMPTY
    # =====================================================

    if not raw_rows:

        return {

            "success": True,

            "message": "No data to transform.",

            "processed_count": 0

        }

    # =====================================================
    # FACT OBJECTS
    # =====================================================

    fact_objects = []

    processed_raw_ids = []

    inserted_count = 0

    updated_count = 0


    now = timezone.now()

    # =====================================================
    # FULL REBUILD
    # =====================================================

    if force_rebuild:

        # =================================================
        # CLEAR BRIDGES
        # =================================================

        PublicationAuthor.objects.all().delete()

        # =================================================
        # CLEAR FACTS
        # =================================================

        FactPublication.objects.all().delete()

        # =================================================
        # CLEAR DIMENSIONS
        # =================================================

        # Cập nhật lại không xóa các bảng này

        #Author.objects.all().delete()

        #University.objects.all().delete()

        #Country.objects.all().delete()

        PublicationRaw.objects.update(
            processed=False,
            processed_at=None
        )


    # =====================================================
    # LOOP RAW ROWS
    # =====================================================

    for raw in raw_rows:

        # =================================================
        # COMPUTE FIELD GROUP
        # =================================================

        field_group = compute_field_group(

            raw.field,

            raw.subfield

        )

        # =================================================
        # COMPUTE CITATION GROUP
        # =================================================

        citation_group = compute_citation_group(

            raw.cited_by
        )

        # =================================================
        # AUTHORSHIP
        # =================================================

        author_count = compute_author_count(

            raw.raw_json.get("Authors")
        )

        is_coauthored = compute_is_coauthored(

            raw.raw_json.get("Authors")
        )

        is_first_author = compute_is_first_author(

            raw.author_affiliations
        )

        # =================================================
        # CORRESPONDING
        # =================================================

        is_corresponding = (

            compute_is_corresponding(

                raw.correspondence_address

            )

        )

        # =================================================
        # COLLABORATION
        # =================================================

        is_international_collaboration = (

            compute_is_international_collaboration(

                raw.author_affiliations

            )

        )

        is_domestic_collaboration = (

            compute_is_domestic_collaboration(

                raw.author_affiliations

            )

        )

        # =================================================
        # UPSERT FACT
        # =================================================

        fact, created = (

            FactPublication.objects.update_or_create(

                publication_raw=raw,

                defaults={

                    # =============================
                    # CORE
                    # =============================

                    "title": raw.title,

                    "year": raw.year,

                    "doi": raw.doi,

                    "cited_by": raw.cited_by,

                    "document_type": (
                        raw.document_type
                    ),
                    "field": (
                        raw.field
                    ),
                    "subfield": (
                        raw.subfield
                    ),
                    "eid": (
                        raw.eid
                    ),
                    "authors_list": (clean_authors(raw.authors)),  
                    # =============================
                    # BUSINESS
                    # =============================
                    "journal": raw.source_title,

                    "field_group": (
                        field_group
                    ),

                    "citation_group": (
                        citation_group
                    ),

                    # =============================
                    # AUTHORSHIP
                    # =============================

                    "author_count": (
                        author_count
                    ),

                    "is_coauthored": (
                        is_coauthored
                    ),

                    "is_first_author": (
                        is_first_author
                    ),

                    "is_corresponding": (
                        is_corresponding
                    ),

                    # =============================
                    # COLLABORATION
                    # =============================

                    "is_international_collaboration": (

                        is_international_collaboration

                    ),

                    "is_domestic_collaboration": (

                        is_domestic_collaboration

                    ),

                    # =============================
                    # TRACKING
                    # =============================

                    "transformed_at": now

                }

            )

        )

        if created:
            inserted_count += 1
        else:
            updated_count += 1

        # =====================================================
        # SAVE DIMENSIONS
        # =====================================================

        dimension_results = (

            save_dimensions(

                raw.author_affiliations

            )

        )

        # =====================================================
        # CREATE PUBLICATION-AUTHOR BRIDGE
        # =====================================================

        for item in dimension_results:

            author_obj = item.get(
                "author_obj"
            )

            if not author_obj:

                continue

            PublicationAuthor.objects.get_or_create(

                publication=fact,

                author=author_obj

            )

        processed_raw_ids.append(
            raw.id
        )

    # =====================================================
    # MARK PROCESSED
    # =====================================================

    PublicationRaw.objects.filter(

        id__in=processed_raw_ids

    ).update(

        processed=True,

        processed_at=now

    )

    # =====================================================
    # RESULT
    # =====================================================

    return {

        "success": True,

        # =============================================
        # COUNTS
        # =============================================

        "processed_count": len(
            processed_raw_ids
        ),

        "inserted_count": inserted_count,

        "updated_count": updated_count,

        # =============================================
        # MESSAGE
        # =============================================

        "message": (

            f"Successfully transformed "

            f"{len(processed_raw_ids)} "

            f"publications."

        )
    }