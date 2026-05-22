from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.dashboard_filter import apply_dashboard_filters
from django.db.models import ( Sum, Count, Q ) 
from dashboard.models import (
    FactPublication,
    Author
)
from dashboard.services.metrics_service import (
    compute_h_index
)

from dashboard.services.author_role_service import(
    get_author_dataset_groupby_field,
    get_author_citation_groupby_field
)


@login_required
def roles_view(request):

    qs = FactPublication.objects.all()

    qs, FIELD_GROUP_ORDER, CITATION_GROUP_ORDER = apply_dashboard_filters(request, qs)

    # ==================================================
    # LQDTU AUTHORS
    # ==================================================

    total_publications = qs.count()
    total_citations = (qs.aggregate(total=Sum("cited_by"))["total"]or 0)

    lqdtu_authors = Author.objects.filter(

        university__name=
        "Le Quy Don Technical University"

    ).distinct()

    total_lqdtu_authors = (
        lqdtu_authors.count()
    )

    # ==================================================
    # FIRST AUTHOR
    # ==================================================

    first_author_qs = (
        FactPublication.objects.filter(
            is_first_author=True
        )
    )

    first_author_publications = (
        first_author_qs.count()
    )

    first_author_citations = (

        first_author_qs.aggregate(

            total=Sum("cited_by")

        )["total"]

        or 0

    )

    first_author_pub_percentage = (

        round(

            first_author_publications
            / total_publications
            * 100,

            1

        )

        if total_publications > 0
        else 0

    )

    first_author_citation_percentage = (

        round(

            first_author_citations
            / total_citations
            * 100,

            1

        )

        if total_citations > 0
        else 0

    )

    first_author_h_index = (
        compute_h_index(

            list(

                first_author_qs.values_list(
                    "cited_by",
                    flat=True
                )

            )

        )
    )

    # ==================================================
    # CORRESPONDING AUTHOR
    # ==================================================

    corresponding_qs = (
        FactPublication.objects.filter(
            is_corresponding=True
        )
    )

    corresponding_publications = (
        corresponding_qs.count()
    )

    corresponding_citations = (

        corresponding_qs.aggregate(

            total=Sum("cited_by")

        )["total"]

        or 0

    )

    corresponding_pub_percentage = (

        round(

            corresponding_publications
            / total_publications
            * 100,

            1

        )

        if total_publications > 0
        else 0

    )

    corresponding_citation_percentage = (

        round(

            corresponding_citations
            / total_citations
            * 100,

            1

        )

        if total_citations > 0
        else 0

    )

    corresponding_h_index = (
        compute_h_index(

            list(

                corresponding_qs.values_list(
                    "cited_by",
                    flat=True
                )

            )

        )
    )

    first_author_datasets, first_author_percentage_values = get_author_dataset_groupby_field(qs, FIELD_GROUP_ORDER, author_role="first_author")

    corr_author_datasets, corr_author_percentage_values = get_author_dataset_groupby_field(qs, FIELD_GROUP_ORDER, author_role="corresponding_author")

    first_author_citation_datasets, first_author_citation_percentage_field = get_author_citation_groupby_field(
        qs, FIELD_GROUP_ORDER, author_role="first_author"
    )
    corr_author_citation_datasets, corr_author_citation_percentage_field = get_author_citation_groupby_field(
        qs, FIELD_GROUP_ORDER, author_role="corresponding_author"
    )

    # ==================================================
    # CONTEXT
    # ==================================================

    context = {

        # TOTAL AUTHORS

        "total_lqdtu_authors":
            total_lqdtu_authors,

        # FIRST AUTHOR

        "first_author_publications":
            first_author_publications,

        "first_author_citations":
            first_author_citations,

        "first_author_pub_percentage":
            first_author_pub_percentage,

        "first_author_citation_percentage":
            first_author_citation_percentage,

        "first_author_h_index":
            first_author_h_index,

        # CORRESPONDING AUTHOR

        "corresponding_publications":
            corresponding_publications,

        "corresponding_citations":
            corresponding_citations,

        "corresponding_pub_percentage":
            corresponding_pub_percentage,

        "corresponding_citation_percentage":
            corresponding_citation_percentage,

        "corresponding_h_index":
            corresponding_h_index,

        "field_group_labels":
            FIELD_GROUP_ORDER,

        "first_author_datasets":
            first_author_datasets,

        "first_author_percentage_values":
            first_author_percentage_values,

        "corr_author_datasets":
            corr_author_datasets,

        "corr_author_percentage_values":              
            corr_author_percentage_values,

        "first_author_citation_datasets":
            first_author_citation_datasets,

        "first_author_citation_percentage_field":              
            first_author_citation_percentage_field,
        
        "corr_author_citation_datasets":
            corr_author_citation_datasets,

        "corr_author_citation_percentage_field":              
            corr_author_citation_percentage_field,

    }

    return render(request, "dashboard/roles.html", context=context)