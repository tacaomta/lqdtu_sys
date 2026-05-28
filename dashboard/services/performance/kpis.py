from django.db.models import ( Sum) 


def get_author_kpis(qs, author_metrics):

    # ==========================================
    # TOTAL AUTHORS
    # ==========================================

    total_authors = len(

        author_metrics

    )


    # ==========================================
    # TOTAL PUBLICATIONS
    # ==========================================

    total_publications = qs.count()


    # ==========================================
    # TOTAL CITATIONS
    # ==========================================

    total_citations = (

        qs.aggregate(

            total=Sum("cited_by")

        )["total"]

        or 0

    )


    # ==========================================
    # PUBLICATION / AUTHOR
    # ==========================================

    publication_per_author = (

        round(

            total_publications
            / total_authors,

            2

        )

        if total_authors > 0

        else 0

    )

    # ==========================================
    # CITATION / AUTHOR
    # ==========================================

    citation_per_author = (

        round(

            total_citations
            / total_authors,

            2

        )

        if total_authors > 0

        else 0

    )

    return publication_per_author, citation_per_author