from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.dashboard_filter import apply_dashboard_filters
from collections import defaultdict
from django.db.models import ( Sum, Count, Q ) 
from dashboard.models import (
    FactPublication,
    PublicationAuthor,
    Author
)
from dashboard.services.metrics_service import (
    compute_h_index
)


@login_required
def performance_view(request):

    qs = FactPublication.objects.all()

    qs, FIELD_GROUP_ORDER, CITATION_GROUP_ORDER = apply_dashboard_filters(request, qs)

    publication_ids = qs.values_list(

        "id",

        flat=True

    )

    author_publication_data = (

        PublicationAuthor.objects.filter(

            publication_id__in=publication_ids

        )

        .values(

            "author_id",

            "publication_id",

            "publication__cited_by"

        )

    )

    author_citations = defaultdict(list) 
    author_publication_counts = defaultdict(set)

    for row in author_publication_data:

        author_id = row["author_id"]

        publication_id = row["publication_id"]

        citation = row["publication__cited_by"] or 0

        author_citations[
            author_id
        ].append(citation)

        author_publication_counts[
            author_id
        ].add(publication_id)


    lqdtu_author_ids = set(

        Author.objects.filter(

            university__name=
            "Le Quy Don Technical University"

        )

        .values_list(

            "id",

            flat=True

        )

    )

    author_metrics = []

    for author_id in author_citations:

        h_index = compute_h_index(author_citations[author_id])

        author_metrics.append({

            "id":
                author_id,

            "publication_count":
                len(

                    author_publication_counts[
                        author_id
                    ]

                ),

            "h_index":
                h_index,
            "is_lqdtu": author_id in lqdtu_author_ids

        })



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
    
    context = { 
        "authors_with_N_publications": author_metrics ,

        "publication_per_author":
        publication_per_author,

        "citation_per_author":
            citation_per_author
    }



    



    return render(request, "dashboard/performance.html", context= context)
