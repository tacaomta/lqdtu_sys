from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.models import (
    FactPublication,
)

from dashboard.services.dashboard_filter import apply_dashboard_filters

from dashboard.services.collaboration.kpis import(
    get_mapping_data,
    get_collaboration_kpis_info
)
from dashboard.services.collaboration.field_collaboration_chart import(
    get_field_collaboration_chart_data
)

@login_required
def collaboration_view(request):

    qs = FactPublication.objects.all()

    qs, FIELD_GROUP_ORDER, CITATION_GROUP_ORDER = apply_dashboard_filters(request, qs)

    publication_ids = qs.values_list(

        "id",

        flat=True

    )

    publication_citation_map = dict(

        FactPublication.objects.filter(

            id__in=publication_ids

        ).values_list(

            "id",

            "cited_by"

        )

    )

    publication_university_country_map = get_mapping_data(publication_ids)

    (
    internal_publication_count,
    internal_h_index,
    external_publication_count,
    external_h_index,
    domestic_publication_count,
    domestic_h_index,
    domestic_collaborator_count,
    domestic_university_count,
    international_publication_count,
    international_h_index,
    international_collaborator_count,
    international_univeristy_count,
    country_count,
    domestic_network,
    international_network
        ) = get_collaboration_kpis_info(publication_ids, publication_university_country_map, publication_citation_map)
    # Các chỉ số KPI tính toàn bộ dữ liệu
    # internal_publication_count, internal_h_index = get_internal_only_publications_info(publication_ids, publication_university_country_map, publication_citation_map)
    # external_publication_count, external_h_index = get_external_publication_info(publication_ids, publication_university_country_map, publication_citation_map)
    # domestic_publication_count, domestic_h_index, domestic_collaborator_count, domestic_university_count = get_domestic_publications_info(publication_ids, publication_university_country_map, publication_citation_map)
    # international_publication_count, international_h_index, international_collaborator_count, international_univeristy_count, country_count = get_international_publications_info(publication_ids, publication_university_country_map, publication_citation_map)
    # Các đồ thị dữ liệu được tính theo nhóm ngành
    (
    field_collaboration_in_ex_datasets, 
    field_in_ex_hindex_datasets, 
    domestic_international_datasets, 
    domestic_international_hindex_datasets,
    domestic_university_ranking,
    international_university_ranking,
    country_ranking
    ) = get_field_collaboration_chart_data(qs, FIELD_GROUP_ORDER, publication_university_country_map, publication_citation_map)
    
   # domestic_university_ranking, international_university_ranking, country_ranking = get_rankings_list(publication_ids, publication_university_country_map)
    
    context = {

        # =====================================
        # PUBLICATIONS
        # =====================================

        "internal_only_publication_count":
            internal_publication_count,

        "external_collaboration_count":
            external_publication_count,

        "domestic_collaboration_count":
            domestic_publication_count,

        "international_collaboration_count":
            international_publication_count,


        # =====================================
        # H-INDEX
        # =====================================

        "internal_hindex":
            internal_h_index,

        "external_hindex":
            external_h_index,

        "domestic_hindex":
            domestic_h_index,

        "international_hindex":
            international_h_index,


        # =====================================
        # AUTHORS
        # =====================================

        "domestic_collaborator_count":
            domestic_collaborator_count,

        "international_collaborator_count":
            international_collaborator_count,


        # =====================================
        # UNIVERSITIES
        # =====================================

        "domestic_partner_university_count":
            domestic_university_count,

        "international_partner_university_count":
            international_univeristy_count,


        # =====================================
        # COUNTRIES
        # =====================================

        "partner_country_count":
            country_count,
        # =====================================
        # CHART
        # =====================================
        "field_collaboration_labels":
            FIELD_GROUP_ORDER,

        "field_collaboration_datasets":
            field_collaboration_in_ex_datasets,
        "field_hindex_datasets":
            field_in_ex_hindex_datasets,
        "domestic_international_datasets":
            domestic_international_datasets,
        "domestic_international_hindex_datasets":
            domestic_international_hindex_datasets,
        
        "domestic_university_ranking":
            domestic_university_ranking,
        "international_university_ranking":
            international_university_ranking,
        "country_ranking":
            country_ranking,
        "domestic_network_nodes":
            domestic_network["nodes"], 
        "domestic_network_edges": domestic_network["edges"],
        "internaltional_network_nodes":
            international_network["nodes"], 
        "internaltional_network_edges": international_network["edges"]
    }

    return render(request, "dashboard/collaboration.html", context=context)