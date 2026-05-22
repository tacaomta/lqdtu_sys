from dashboard.services.filter_service import get_years
from dashboard.services.citation_service import (
    get_citation_groups
)
from dashboard.services.field_group_service import(
    get_field_groups
)

from dashboard.models.import_batch import (
    ImportBatch
)


def global_filters(request):
    selected_years = request.GET.getlist("years")
    selected_fields = request.GET.getlist("fields")
    first = request.GET.get("first") == "true"
    corresponding = request.GET.get("corresponding") == "true"
    selected_citations = request.GET.getlist("citations")
    

    return {
        "years": get_years(),
        "fields": get_field_groups(),

        # selected values
        "selected_years": selected_years,
        "selected_fields": selected_fields,

        # trạng thái filter
        "is_filtering_years": bool(selected_years),
        "is_filtering_fields": bool(selected_fields),

        "first_selected": first,
        "corresponding_selected": corresponding,
        "first_checked":
            'checked="checked"' if first else "",

        "is_filtering_roles": first or corresponding,
        "corresponding_checked":
            'checked="checked"' if corresponding else "",
        "citation_groups": get_citation_groups(),

        "selected_citations": selected_citations,

        "is_filtering_citations": bool(selected_citations),
        "querystring":
            request.GET.urlencode(),
    }


def global_scopus_info(request):

    latest_batch = (

        ImportBatch.objects

        .filter(status="COMPLETED")

        .order_by("-id")

        .first()

    )

    return {

        "latest_scopus_batch": latest_batch

    }