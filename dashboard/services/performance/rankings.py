from collections import defaultdict

from dashboard.models import (
    PublicationAuthor,
    Author
)

from dashboard.services.metrics_service import (
    compute_h_index
)

def get_ranking_tables(qs, author_metrics, FIELD_GROUP_ORDER):

    top_publication_authors = sorted(

        author_metrics,

        key=lambda x: x["publication_count"],

        reverse=True
    )

    top_citation_authors = sorted(

        author_metrics,

        key=lambda x: x["citation_count"],

        reverse=True
    )

    top_hindex_authors = sorted(

        author_metrics,

        key=lambda x: x["h_index"],

        reverse=True
    )
    field_author_tables = {}

    field_author_tables["Tất cả"] = {

        "label": "Không phân nhóm",

        "publication": top_publication_authors,

        "citation": top_citation_authors,

        "hindex": top_hindex_authors
    }

    for field_group in FIELD_GROUP_ORDER:

        # =====================================
        # FILTER FIELD
        # =====================================

        field_qs = qs.filter(

            field_group=field_group

        )


        publication_ids = field_qs.values_list(

            "id",

            flat=True

        )


        # =====================================
        # AUTHOR PUBLICATION DATA
        # =====================================

        author_publication_data = (

            PublicationAuthor.objects.filter(

                publication_id__in=publication_ids,
                author__university__name = "Le Quy Don Technical University"

            )

            .values(

                "author_id",

                "publication_id",

                "publication__cited_by"

            )

        )

        # =====================================
        # BUILD DICTS
        # =====================================


        author_citations = defaultdict(list)

        author_publication_counts = defaultdict(set)


        for row in author_publication_data:

            author_id = row["author_id"]

            publication_id = row["publication_id"]

            citation = row["publication__cited_by"] or 0


            author_citations[
                author_id
            ].append(citation)


            author_publication_counts[
                author_id
            ].add(publication_id)


        # =====================================
        # AUTHOR NAME MAP
        # =====================================

        author_name_map = dict(

            Author.objects.filter(

                id__in=author_citations.keys()

            )

            .values_list(

                "id",

                "name"

            )

        )


        # =====================================
        # BUILD METRICS
        # =====================================

        field_author_metrics = []


        for author_id in author_citations:

            citations = sorted(

                author_citations[author_id],

                reverse=True

            )


            h_index = compute_h_index(

                citations

            )


            citation_count = sum(

                citations

            )


            field_author_metrics.append({

                "id":
                    author_id,

                "author_name":
                    author_name_map.get(
                        author_id,
                        "-"
                    ),

                "publication_count":
                    len(

                        author_publication_counts[
                            author_id
                        ]

                    ),

                "citation_count":
                    citation_count,

                "h_index":
                    h_index

            })

        field_author_tables[field_group] = {

            "publication":

                sorted(

                    field_author_metrics,

                    key=lambda x:
                        x["publication_count"],

                    reverse=True

                ),

            "citation":

                sorted(

                    field_author_metrics,

                    key=lambda x:
                        x["citation_count"],

                    reverse=True

                ),

            "hindex":

                sorted(

                    field_author_metrics,

                    key=lambda x:
                        x["h_index"],

                    reverse=True

                )

        }

    return field_author_tables

