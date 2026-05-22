import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import (
    Sum,
    Avg,
    Max,
    Count
)

from dashboard.models import (
    FactPublication,
    ImportBatch
)

from dashboard.services.dashboard_filter import(
    apply_dashboard_filters
)


@login_required
def citations_view(request):

    qs = FactPublication.objects.all()

    qs, FIELD_GROUP_ORDER, CITATION_GROUP_ORDER = apply_dashboard_filters(request, qs)

    total_citations = (qs.aggregate(total=Sum("cited_by"))["total"]or 0)

    total_publications = qs.count()

    citation_per_publication = 0

    if total_publications > 0:
        citation_per_publication = round(
            total_citations
            / total_publications,
            2
        )

    max_citation = (qs.aggregate(max_value=Max("cited_by"))["max_value"]or 0)

    # Top 10% cited publication
    sorted_citations = list(

        qs.values_list(

            "cited_by",

            flat=True

        ).order_by("-cited_by")

    )

    top_10_count = int(len(sorted_citations) * 0.1)

    uncited_count = qs.filter(cited_by=0).count()

    uncited_percentage = 0

    if total_publications > 0:

        uncited_percentage = round(uncited_count/ total_publications * 100, 2)

    first_year = qs.order_by("year").values_list("year",flat=True).first()

    latest_batch = (ImportBatch.objects.exclude(data_updated_until__isnull=True).order_by("-id").first())
    updated_year = None

    if latest_batch:

        updated_year = (

            latest_batch
            .data_updated_until
            .year

        )

    year_span = 1

    if first_year and updated_year:

        year_span = max(

            updated_year
            - first_year
            + 1,

            1

        )
    citation_per_year = round(total_citations/ year_span,2)
    
    # Đồ thị
    citation_by_year_qs = (
    qs.values("year")
    .annotate(

        total_citations=Sum("cited_by")

    )
    .order_by("year"))

    citation_lookup = {

    item["year"]: item["total_citations"]

    for item in citation_by_year_qs

    }

    min_year = min(citation_lookup.keys())

    max_year = max(citation_lookup.keys())

    all_years = list(

        range(

            min_year,
            max_year + 1

        )

    )
    raw_values = [citation_lookup.get(year, 0) for year in all_years]

    ## Biểu đồ stacked số CBKH theo nhóm trích dẫn



    field_citation_qs = (

        qs.values("field_group", "citation_group")

        .annotate(

            total=Count("id")

        )

    )

    stacked_lookup = {}

    for item in field_citation_qs:

        field_group = item["field_group"]

        citation_group = item["citation_group"]

        total = item["total"]

        if field_group not in stacked_lookup:

            stacked_lookup[field_group] = {}

        stacked_lookup[field_group][citation_group] = total
    

        stacked_datasets = []

        for citation_group in CITATION_GROUP_ORDER:

            data = []

            for field_group in FIELD_GROUP_ORDER:

                value = (

                    stacked_lookup

                    .get(field_group, {})

                    .get(citation_group, 0)

                )

                data.append(value)

            stacked_datasets.append({

                "label": citation_group,

                "data": data

            })

    # Pie chart
    # ==========================================
    # PIE CHART — CITATION GROUP DISTRIBUTION
    # ==========================================

    citation_group_qs = (

        qs.values("citation_group")

        .annotate(

            total=Count("id")

        )

    )

    # ==========================================
    # LOOKUP
    # ==========================================

    citation_group_lookup = {

        item["citation_group"]: item["total"]

        for item in citation_group_qs

    }

    # ==========================================
    # ORDERED LABELS
    # ==========================================

    citation_group_labels = [

        group

        for group in CITATION_GROUP_ORDER

    ]

    # ==========================================
    # ORDERED VALUES
    # ==========================================

    citation_group_values = [

        citation_group_lookup.get(
            group,
            0
        )

        for group in citation_group_labels

    ]

    #Row 3
    field_citation_sum_qs = (

        qs.values(

            "field_group",
            "citation_group"

        )

        .annotate(

            total_citations=Sum("cited_by")

        )

    )

    citation_sum_lookup = {}

    for item in field_citation_sum_qs:

        field_group = item["field_group"]

        citation_group = item["citation_group"]

        total_citations_field = (

            item["total_citations"]

            or 0

        )

        if field_group not in citation_sum_lookup:

            citation_sum_lookup[field_group] = {}

        citation_sum_lookup[

            field_group

        ][citation_group] = total_citations_field

    citation_sum_datasets = []

    for citation_group in CITATION_GROUP_ORDER:

        data = []

        for field_group in FIELD_GROUP_ORDER:

            value = (

                citation_sum_lookup

                .get(field_group, {})

                .get(citation_group, 0)

            )

            data.append(value)

        citation_sum_datasets.append({

            "label": citation_group,

            "data": data

        })

    ## Tree map
    field_total_citation_qs = (

        qs.values("field_group")

        .annotate(

            total_citations=Sum("cited_by")

        )

    )

    field_total_citation_lookup = {

        item["field_group"]:

        item["total_citations"] or 0

        for item in field_total_citation_qs

    }

    treemap_labels = [field for field in FIELD_GROUP_ORDER]
    treemap_values = [field_total_citation_lookup.get(field,0) for field in treemap_labels]

    # ==========================================
    # CITATION BY DOCUMENT TYPE IN FIELD GROUP
    # ==========================================

    document_citation_qs = (

        qs.values(

            "field_group",
            "document_type"

        )

        .annotate(

            total_citations=Sum(
                "cited_by"
            )

        )

    )

    document_types = list(

        qs.values_list(

            "document_type",
            flat=True

        )

        .distinct()

    )

    # ==========================================
    # BUILD MATRIX
    # ==========================================

    document_type_datasets = []
    

    for document_type in document_types:

        values = []

        for field_group in FIELD_GROUP_ORDER:

            item = next(

                (

                    x for x in document_citation_qs

                    if (

                        x["field_group"]
                        == field_group

                        and

                        x["document_type"]
                        == document_type

                    )

                ),

                None

            )

            values.append(

                item["total_citations"]

                if item else 0

            )

        document_type_datasets.append({

            "label": document_type,

            "data": values

        })
    # ==========================================
    # ARTICLE CITATION PERCENTAGE
    # ==========================================

    article_percentage_values = []

    for field_group in FIELD_GROUP_ORDER:

        group_items = [

            x for x in document_citation_qs

            if x["field_group"] == field_group

        ]

        total_citations_each_field = sum(

            x["total_citations"]
            or 0

            for x in group_items

        )

        article_citations = sum(

            x["total_citations"]
            or 0

            for x in group_items

            if x["document_type"] == "Article"

        )

        percentage = (

            round(

                article_citations
                / total_citations_each_field
                * 100,

                2

            )

            if total_citations_each_field > 0

            else 0

        )

        article_percentage_values.append(
            percentage
        )

    # ==========================================
    # DOCUMENT TYPE CITATION PIE CHART
    # ==========================================

    document_type_pie_qs = (

        qs.values(

            "document_type"

        )

        .annotate(

            total_citations=Sum(
                "cited_by"
            )

        )

        .order_by(

            "-total_citations"

        )

    )

    document_type_pie_labels = [ x["document_type"] for x in document_type_pie_qs ]

    document_type_pie_values = [

        x["total_citations"]

        for x in document_type_pie_qs

    ]


    context = {

        "total_citations":
            total_citations,

        "citation_per_publication":
            citation_per_publication,

        "max_citation":
            max_citation,

        "highly_cited_count":
            top_10_count,

        "uncited_count":
            uncited_count,

        "uncited_percentage":
            uncited_percentage,

        "citation_per_year":
            citation_per_year,

        "citation_years":
        all_years,

        "citation_values":
            raw_values,

        "field_group_labels": FIELD_GROUP_ORDER, 
        "stacked_datasets": stacked_datasets,

        "citation_group_labels":citation_group_labels,

        "citation_group_values": citation_group_values,

        "citation_sum_datasets": citation_sum_datasets,

        "treemap_labels":treemap_labels,
        
        "treemap_values":treemap_values,

        "document_type_datasets": document_type_datasets,

        "article_percentage_values": article_percentage_values,

        "document_type_pie_labels": document_type_pie_labels,

        "document_type_pie_values": document_type_pie_values

    }
    return render(request, "dashboard/citations.html", context= context)
