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


@login_required
def performance_view(request):

    qs = FactPublication.objects.all()

    qs, FIELD_GROUP_ORDER, CITATION_GROUP_ORDER = apply_dashboard_filters(request, qs)

    publication_ids = qs.values_list(

        "publication_raw_id",

        flat=True

    )
    authors_qs = (

        Author.objects.filter(

            publication_authors__publication_id__in=

            publication_ids

        )
        .distinct()
    )

    authors_qs = (

        authors_qs.annotate(

            publication_count=Count(

                "publication_authors__publication",
                distinct=True
            )
        ).distinct()
    )

    authors_with_N_publications = list(authors_qs.values( "id", "publication_count" ) )
    context = { 
        "authors_with_N_publications": authors_with_N_publications 
    }



    



    return render(request, "dashboard/performance.html", context= context)
