from django.db.models import Sum


def get_author_dataset_groupby_field(qs, field_group_order, author_role="first_author"):
    author_lqd_values = []

    author_non_lqd_values = []

    author_percentage_values = []
    table_rows= []

    for field_group in field_group_order:
        if author_role=="first_author":

            field_qs = qs.filter(

                field_group=field_group

            )

            lqd_count = (

                field_qs.filter(

                    is_first_author=True

                )

                .count()

            )

            non_lqd_count = (

                field_qs.filter(

                    is_first_author=False

                )

                .count()

            )

            total_count = (
                lqd_count +
                non_lqd_count
            )

            percentage = (round(lqd_count/ total_count* 100, 1) if total_count > 0 else 0)
        else:
            field_qs = qs.filter(

            field_group=field_group

            )

            lqd_count = (

                field_qs.filter(

                    is_corresponding=True

                )

                .count()

            )

            non_lqd_count = (

                field_qs.filter(

                    is_corresponding=False

                )

                .count()

            )

            total_count = (
                lqd_count +
                non_lqd_count
            )

            percentage = (

                round(

                    lqd_count
                    / total_count
                    * 100,

                    1

                )

                if total_count > 0

                else 0

            )

        author_lqd_values.append(
            lqd_count
        )

        author_non_lqd_values.append(
            non_lqd_count
        )

        author_percentage_values.append(
            percentage
        )

        table_rows.append({

            "group":

                field_group,

            "values": [

                lqd_count,

                non_lqd_count,
                percentage

            ]

        })
    
    col_labels = ["LQDTU", "Không thuộc LQDTU", '% LQDTU']


    author_datasets = [

        {

            "label":
                "CBKH có tác giả thứ nhất thuộc LQDTU" if author_role=="first_author" else "CBKH có tác giả liên hệ thuộc LQDTU",

            "data":
                author_lqd_values

        },

        {

            "label":
                "CBKH có tác giả thứ nhất không thuộc LQDTU" if author_role=="first_author" else "CBKH có tác giả liên hệ không thuộc LQDTU",

            "data":
                author_non_lqd_values

        }

    ]
    return author_datasets, author_percentage_values, table_rows, col_labels


def get_author_citation_groupby_field(qs, field_group_order, author_role="first_author"):

    author_lqd_citations = []

    author_non_lqd_citations = []

    author_citation_percentage = []

    table_rows = []

    for field_group in field_group_order:

        if author_role=="first_author":

            field_qs = qs.filter(

                field_group=field_group

            )

            lqd_citations = (

                field_qs.filter(

                    is_first_author=True

                )

                .aggregate(

                    total=Sum("cited_by")

                )["total"]

                or 0

            )

            non_lqd_citations = (

                field_qs.filter(

                    is_first_author=False

                )

                .aggregate(

                    total=Sum("cited_by")

                )["total"]

                or 0

            )

            total_citations = (

                lqd_citations +
                non_lqd_citations

            )

            percentage = (

                round(

                    lqd_citations
                    / total_citations
                    * 100,

                    1

                )

                if total_citations > 0

                else 0

            )
        else:
            field_qs = qs.filter(

                field_group=field_group

            )

            lqd_citations = (

                field_qs.filter(

                    is_corresponding=True

                )

                .aggregate(

                    total=Sum("cited_by")

                )["total"]

                or 0

            )

            non_lqd_citations = (

                field_qs.filter(

                    is_corresponding=False

                )

                .aggregate(

                    total=Sum("cited_by")

                )["total"]

                or 0

            )

            total_citations = (

                lqd_citations +
                non_lqd_citations

            )

            percentage = (

                round(

                    lqd_citations
                    / total_citations
                    * 100,

                    1

                )

                if total_citations > 0

                else 0

            )

        author_lqd_citations.append(
            lqd_citations
        )

        author_non_lqd_citations.append(
            non_lqd_citations
        )

        author_citation_percentage.append(
            percentage
        )
    
        table_rows.append({

                "group":

                    field_group,

                "values": [

                    lqd_citations,

                    non_lqd_citations,
                    percentage

                ]

            })


    author_citation_datasets = [

        {

            "label":
                "Trích dẫn từ CBKH có tác giả thứ nhất thuộc LQDTU" if author_role=="first_author" else "Trích dẫn từ CBKH có tác giả liên hệ thuộc LQDTU",

            "data":
                author_lqd_citations

        },

        {

            "label":
                "Trích dẫn từ CBKH có tác giả thứ nhất không thuộc LQDTU" if author_role=="first_author" else "Trích dẫn từ CBKH có tác giả liên hệ không thuộc LQDTU",

            "data":
                author_non_lqd_citations

        }

    ]
    return author_citation_datasets, author_citation_percentage, table_rows
