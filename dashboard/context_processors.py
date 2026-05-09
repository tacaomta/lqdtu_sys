from dashboard.services.filter_service import get_years, get_fields, get_citation_groups

def global_filters(request):
    selected_years = request.GET.getlist("years")
    selected_fields = request.GET.getlist("fields")
    first = request.GET.get("first") == "true"
    corresponding = request.GET.get("corresponding") == "true"
    selected_citations = request.GET.getlist("citations")
    

    return {
        "years": get_years(),
        "fields": get_fields(),

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