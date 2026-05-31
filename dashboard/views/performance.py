from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.dashboard_filter import apply_dashboard_filters
from dashboard.models import (
    FactPublication
)

from dashboard.services.performance.author_metrics import(
    get_author_metrics
)

from dashboard.services.performance.kpis import(
    get_author_kpis
)
from dashboard.services.performance.histograms import(
    get_author_histograms
)
from dashboard.services.performance.rankings import(
    get_ranking_tables
)


@login_required
def performance_view(request):

    qs = FactPublication.objects.all()

    qs, FIELD_GROUP_ORDER, CITATION_GROUP_ORDER = apply_dashboard_filters(request, qs)

    has_data = qs.exists()

    if not has_data:
        return render(request, "dashboard/performance.html", context= {"has_data": has_data})

    author_metrics = get_author_metrics(qs=qs)

    publication_per_author, citation_per_author = get_author_kpis(qs, author_metrics)

    # ==========================================
    # HISTOGRAM - PUBLICATION COUNT
    # ==========================================
    publication_bins, publication_bin_counts, citation_bins, citation_bin_values = get_author_histograms(author_metrics)
    
    # ==========================================
    # SORTED TABLES
    # ==========================================
    field_author_tables = get_ranking_tables(qs, author_metrics, FIELD_GROUP_ORDER)
    
    context = { 
        "has_data": has_data,

        "authors_with_N_publications": 
        author_metrics ,

        "publication_per_author":
        publication_per_author,

        "citation_per_author":
            citation_per_author,
        
        "publication_bins":
            publication_bins,

        "publication_bin_counts":
            publication_bin_counts,

        "citation_bins":
            citation_bins,

        "citation_bin_counts":
            citation_bin_values,

        "field_author_tables":
            field_author_tables
    }

    return render(request, "dashboard/performance.html", context= context)
