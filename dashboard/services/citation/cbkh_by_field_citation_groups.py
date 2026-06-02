from django.db.models import (
    Count
)



def get_cbkh_by_field_citation_groups(qs, CITATION_GROUP_ORDER, FIELD_GROUP_ORDER):

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
        
    # Dữ liệu dạng bảng của cái này
    tb_CBKH_field_citation_group_rows = []

    for field_group in FIELD_GROUP_ORDER:

        row = {

            "group": field_group,

            "values": []

        }

        for citation_group in CITATION_GROUP_ORDER:

            value = (

                stacked_lookup

                .get(field_group, {})

                .get(citation_group, 0)

            )

            row["values"].append(value)

        tb_CBKH_field_citation_group_rows.append(row)
    
    return stacked_datasets, tb_CBKH_field_citation_group_rows