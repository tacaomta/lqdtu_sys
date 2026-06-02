from django.db.models import (
    Sum
)


def get_total_citation_by_field_citation_groups(qs, CITATION_GROUP_ORDER, FIELD_GROUP_ORDER):
    field_citation_sum_qs = (

        qs.values(

            "field_group",
            "citation_group"

        )

        .annotate(

            total_citations=Sum("cited_by")

        )

    )

    citation_sum_lookup = {}

    for item in field_citation_sum_qs:

        field_group = item["field_group"]

        citation_group = item["citation_group"]

        total_citations_field = (

            item["total_citations"]

            or 0

        )

        if field_group not in citation_sum_lookup:

            citation_sum_lookup[field_group] = {}

        citation_sum_lookup[

            field_group

        ][citation_group] = total_citations_field

    citation_sum_datasets = []

    for citation_group in CITATION_GROUP_ORDER:

        data = []

        for field_group in FIELD_GROUP_ORDER:

            value = (

                citation_sum_lookup

                .get(field_group, {})

                .get(citation_group, 0)

            )

            data.append(value)

        citation_sum_datasets.append({

            "label": citation_group,

            "data": data

        })
    
    tb_total_citation_field_citation_group_rows = []

    for field_group in FIELD_GROUP_ORDER:

        row = {

            "group": field_group,

            "values": []

        }

        for citation_group in CITATION_GROUP_ORDER:

            value = (

                citation_sum_lookup

                .get(field_group, {})

                .get(citation_group, 0)

            )

            row["values"].append(value)

        tb_total_citation_field_citation_group_rows.append(row)
    
    return citation_sum_datasets, tb_total_citation_field_citation_group_rows


def get_citation_by_field_document_type(qs, FIELD_GROUP_ORDER):
    document_citation_qs = (

        qs.values(

            "field_group",
            "document_type"

        )

        .annotate(

            total_citations=Sum(
                "cited_by"
            )

        )

    )
    citation_lookup = {}

    for item in document_citation_qs:

        citation_lookup[(

            item["field_group"],

            item["document_type"]

        )] = item["total_citations"] or 0

    document_types = list(

        qs.values_list(

            "document_type",
            flat=True

        )

        .distinct()

    )

    # ==========================================
    # BUILD MATRIX
    # ==========================================

    document_type_datasets = []

    for document_type in document_types:

        values = []

        for field_group in FIELD_GROUP_ORDER:

            values.append(

                citation_lookup.get(

                    (

                        field_group,

                        document_type

                    ),

                    0

                )

            )

        document_type_datasets.append({

            "label": document_type,

            "data": values

        })
    
    # ==========================================
    # ARTICLE CITATION PERCENTAGE
    # ==========================================

    article_percentage_values = []

    for field_group in FIELD_GROUP_ORDER:

        group_items = [

            x for x in document_citation_qs

            if x["field_group"] == field_group

        ]

        total_citations_each_field = sum(

            x["total_citations"]
            or 0

            for x in group_items

        )

        article_citations = sum(

            x["total_citations"]
            or 0

            for x in group_items

            if x["document_type"] == "Article"

        )

        percentage = (

            round(

                article_citations
                / total_citations_each_field
                * 100,

                1

            )

            if total_citations_each_field > 0

            else 0

        )

        article_percentage_values.append(
            percentage
        )

    table_rows = []

    for idx, field_group in enumerate(

        FIELD_GROUP_ORDER

    ):

        row = {

            "group": field_group,

            "values": []

        }

        for document_type in document_types:

            value = citation_lookup.get(

                (

                    field_group,

                    document_type

                ),

                0

            )

            row["values"].append(

                value

            )

        row["values"].append(article_percentage_values[idx])

        table_rows.append(row)
    
    document_types.append("% Trích dẫn từ Article")
    
    return document_type_datasets, article_percentage_values, table_rows, document_types
