from dashboard.models.fact import (
    FactPublication
)
from dashboard.services.field_group_service import (get_field_groups)
from dashboard.services.citation_service import(get_citation_groups)


# =====================================================
# APPLY DASHBOARD FILTERS
# =====================================================

def apply_dashboard_filters(

    request,

    qs=None

):
    CITATION_GROUP_ORDER = [i[0] for i in get_citation_groups()]
    FIELD_GROUP_ORDER = get_field_groups()

    citation_group = request.GET.getlist(
        "citations"
    )

    # ==============================================
    # BASE QUERYSET
    # ==============================================

    if qs is None:

        qs = FactPublication.objects.all()

    # ==============================================
    # YEAR
    # ==============================================


    selected_years = request.GET.getlist(
        "years"
    )

    if selected_years:

        qs = qs.filter(
            year__in=selected_years
        )

    # ==============================================
    # FIELD GROUP
    # ==============================================

    field_group = request.GET.getlist(
        "fields"
    )

    if field_group:

        qs = qs.filter(
            field_group__in=field_group
        )
        FIELD_GROUP_ORDER = [i for i in FIELD_GROUP_ORDER if i in field_group]

    # ==============================================
    # FIRST AUTHOR
    # ==============================================

    is_first_author = request.GET.get(
        "first"
    )

    if is_first_author in [

        "true",
        "false"

    ]:

        qs = qs.filter(

            is_first_author=(
                is_first_author == "true"
            )

        )

    # ==============================================
    # CORRESPONDING AUTHOR
    # ==============================================

    is_corresponding = request.GET.get(
        "corresponding"
    )

    if is_corresponding in [

        "true",
        "false"

    ]:

        qs = qs.filter(

            is_corresponding=(
                is_corresponding == "true"
            )

        )

    # ==============================================
    # CITATION GROUP
    # ==============================================

    citation_group = request.GET.getlist(
        "citations"
    )

    if citation_group:

        qs = qs.filter(
            citation_group__in=citation_group
        )
        CITATION_GROUP_ORDER = [i for i in CITATION_GROUP_ORDER if i in citation_group]

    return qs, FIELD_GROUP_ORDER, CITATION_GROUP_ORDER