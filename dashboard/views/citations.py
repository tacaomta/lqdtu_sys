from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import (
    Sum,
    Max,
    Count
)

from dashboard.models import (
    FactPublication,
    ImportBatch
)

from dashboard.services.citation.cbkh_by_field_citation_groups import(
    get_cbkh_by_field_citation_groups
)

from dashboard.services.dashboard_filter import(
    apply_dashboard_filters
)
from dashboard.services.citation.citation_by_field_citation_groups import(
    get_total_citation_by_field_citation_groups,
    get_citation_by_field_document_type,
    get_percentage_citation_by_fields
)
from dashboard.services.metrics_service import(
    format_number
)
from dashboard.services.config_service import is_dirty


@login_required
def citations_view(request):

    qs = FactPublication.objects.all()

    qs, FIELD_GROUP_ORDER, CITATION_GROUP_ORDER = apply_dashboard_filters(request, qs)

    has_data = qs.exists()

    if not has_data:
        return render(request, "dashboard/citations.html", context= {"has_data": has_data})

    total_citations = (qs.aggregate(total=Sum("cited_by"))["total"]or 0)

    total_publications = qs.count()

    citation_per_publication = 0

    if total_publications > 0:
        citation_per_publication = round(
            total_citations
            / total_publications,
            1
        )

    max_citation = (qs.aggregate(max_value=Max("cited_by"))["max_value"]or 0)

    # Top 10% cited publication
    sorted_citations = list(
        qs.filter(cited_by__gt=0)
        .values_list(

            "cited_by",

            flat=True

        ).order_by("-cited_by")

    )

    top_10_count = int(len(sorted_citations) * 0.1)

    uncited_count = qs.filter(cited_by=0).count()

    uncited_percentage = 0

    if total_publications > 0:

        uncited_percentage = round(uncited_count/ total_publications * 100, 1)

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
    citation_per_year = round(total_citations/ year_span, 1)
    
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

    ## Biểu đồ + dữ liệu dạng bảng stacked số CBKH theo nhóm trích dẫn
    stacked_datasets, tb_CBKH_field_citation_group_rows = get_cbkh_by_field_citation_groups(qs, CITATION_GROUP_ORDER, FIELD_GROUP_ORDER)

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

    citation_group_values = [

        citation_group_lookup.get(
            group,
            0
        )

        for group in CITATION_GROUP_ORDER

    ]

    #Row 3
    citation_sum_datasets, tb_total_citation_field_citation_group_rows = get_total_citation_by_field_citation_groups(qs, CITATION_GROUP_ORDER, FIELD_GROUP_ORDER)
    

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

    document_type_datasets, article_percentage_values, citation_by_field_document_type_table_rows, document_type_labels = get_citation_by_field_document_type(qs, FIELD_GROUP_ORDER)
    # ==========================================
    # DOCUMENT TYPE CITATION PIE CHART
    # ==========================================

    document_type_pie_values, document_type_pie_labels = get_percentage_citation_by_fields(qs)


    context = {
        "has_data": has_data,

        "config_dirty": is_dirty(),

        "total_citations":
            format_number(total_citations),

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
            format_number(citation_per_year),

        "citation_years":
        all_years,

        "citation_values":
            raw_values,

        "field_group_labels": FIELD_GROUP_ORDER, 
        "stacked_datasets": stacked_datasets,

        "cbkh_table_row": tb_CBKH_field_citation_group_rows,

        "citation_group_labels":CITATION_GROUP_ORDER,

        "citation_group_values": citation_group_values,

        "citation_sum_datasets": citation_sum_datasets,

        "citation_by_groupcited_table_row": tb_total_citation_field_citation_group_rows,

        "treemap_labels":treemap_labels,
        
        "treemap_values":treemap_values,

        "document_type_datasets": document_type_datasets,

        "citation_by_dt_fields":citation_by_field_document_type_table_rows,
        "document_type_labels": document_type_labels,

        "article_percentage_values": article_percentage_values,

        "document_type_pie_labels": document_type_pie_labels,

        "document_type_pie_values": document_type_pie_values

    }
    return render(request, "dashboard/citations.html", context= context)
