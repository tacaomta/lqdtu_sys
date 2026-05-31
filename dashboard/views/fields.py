from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from dashboard.services.chart_service import(
    build_chart_dataset,
    build_stacked_chart_dataset
)
from dashboard.models.fact import(
    FactPublication
)
from dashboard.services.dashboard_filter import(
    apply_dashboard_filters
)

from dashboard.services.metrics_service import (
    compute_h_index
)


@login_required
def fields_view(request):
    qs = FactPublication.objects.all()
    qs, FIELD_GROUP_ORDER, CITATION_GROUP_ORDER = apply_dashboard_filters(request, qs)
    has_data = qs.exists()

    if not has_data:
        return render(request, "dashboard/fields.html", context= {"has_data": has_data})

    field_chart = build_chart_dataset(qs=qs, group_field="field_group", custom_order=FIELD_GROUP_ORDER)

    stacked_chart = build_stacked_chart_dataset(

        qs=qs,

        x_field="field_group",

        stack_field="document_type",

        x_order=FIELD_GROUP_ORDER

    )

    # ==========================================
    # ARTICLE PERCENTAGE
    # ==========================================

    article_qs = (

        qs.values("field_group")

        .annotate(

            total=Count("id"),

            article_count=Count(

                "id",

                filter=Q(
                    document_type="Article"
                )

            )

        )
    )

    article_lookup = {}

    for item in article_qs:

        total = item["total"]

        article_count = item["article_count"]

        percentage = 0

        if total > 0:

            percentage = round(

                article_count / total * 100,

                1

            )

        article_lookup[

            item["field_group"]

        ] = percentage

    article_labels = [

        label

        for label in FIELD_GROUP_ORDER

        if label in article_lookup

    ]

    article_values = [

        article_lookup[label]

        for label in article_labels

    ]

    # ==========================================
    # FIELD H-INDEX
    # ==========================================

    field_hindex_lookup = {}

    for field_group in FIELD_GROUP_ORDER:

        field_qs = qs.filter(

            field_group=field_group

        )

        citations = list(

            field_qs.values_list(

                "cited_by",

                flat=True

            )

        )

        citations = [

            c if c else 0

            for c in citations

        ]

        h_index = compute_h_index(citations)

        field_hindex_lookup[field_group] = h_index
    
    hindex_labels = [label for label in FIELD_GROUP_ORDER if label in field_hindex_lookup]

    hindex_values = [field_hindex_lookup[label] for label in hindex_labels]



    context = {
        "has_data": has_data,

        "field_labels":
            field_chart["labels"],

        "field_values":
            field_chart["values"],

        "stacked_labels": stacked_chart["labels"], 
        
        "stacked_datasets": stacked_chart["datasets"],

        "article_labels": article_labels, 
        
        "article_values": article_values,

        "hindex_labels": hindex_labels, 
        
        "hindex_values": hindex_values

    }
    return render( request, "dashboard/fields.html", context)
