from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.db.models import (
    Count,
    Sum,
    Avg
)

from dashboard.models.fact import (
    FactPublication
)
from dashboard.services.dashboard_filter import(
    apply_dashboard_filters
)

from dashboard.services.metrics_service import (
    compute_h_index,
    format_number
)

from datetime import datetime


# Create your views here.
@login_required
def overview_view(request):
    current_year = datetime.now().year

    qs = FactPublication.objects.all()
    qs, FIELD_GROUP_ORDER, CITATION_GROUP_ORDER = apply_dashboard_filters(request, qs)

    has_data = qs.exists()

    if not has_data:
        return render(request, "dashboard/overview.html", context= {"has_data": has_data})
    # ======================================
    # KPI
    # ======================================

    total_publications = qs.count()

    publications_this_year = qs.filter(
        year=current_year
    ).count()

    first_year = qs.order_by("year") \
        .values_list("year", flat=True) \
        .first()

    year_count = max(

        qs.values("year")
        .distinct()
        .count(),
        1

    )

    publications_per_year = round(
        total_publications / year_count,
        2
    )


    total_citations = qs.aggregate(
        total=Sum("cited_by")
    )["total"] or 0

    avg_citation = round(
        total_citations / total_publications,
        2
    ) if total_publications else 0

    citations = list(
        qs.values_list(
            "cited_by",
            flat=True
        )
    )

    h_index = compute_h_index(
        citations
    )

    # ======================================
    # PUBLICATION TREND
    # ======================================

    publication_by_year = (

        qs.values("year")

        .annotate(
            total=Count("id")
        )

        .order_by("year")

    )

    publication_years = [
        x["year"]
        for x in publication_by_year
    ]

    publication_counts = [
        x["total"]
        for x in publication_by_year
    ]

    # ======================================
    # CITATION TREND
    # ======================================

    citation_by_year = (

        qs.values("year")

        .annotate(
            total=Sum("cited_by")
        )

        .order_by("year")

    )

    citation_counts = [
        x["total"] or 0
        for x in citation_by_year
    ]

    context = {
        "has_data": has_data,
        # KPI
        "total_publications": format_number(total_publications),

        "publications_this_year": publications_this_year,

        "publications_per_year": publications_per_year,

        "total_citations": format_number(total_citations),

        "avg_citation": avg_citation,

        "h_index": h_index,

        # CHART
        "publication_years": publication_years,

        "publication_counts": publication_counts,

        "citation_counts": citation_counts,

    }

    return render(

        request,

        "dashboard/overview.html",

        context

    )