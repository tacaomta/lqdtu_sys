from collections import defaultdict

from dashboard.models import (
    PublicationAuthor,
    Author
)

from dashboard.services.metrics_service import (
    compute_h_index
)



def get_author_metrics(qs):

    publication_ids = qs.values_list(

            "id",

            flat=True

        )

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

    author_name_map = dict(

        Author.objects.filter(

            id__in=author_citations.keys()

        )

        .values_list(

            "id",

            "name"

        )
    )


    author_metrics = []

    for author_id in author_citations:

        h_index = compute_h_index(author_citations[author_id])

        author_metrics.append({

            "id":
                author_id,

            "author_name":
                author_name_map.get(author_id, "-"),

            "publication_count":
                len(

                    author_publication_counts[
                        author_id
                    ]

                ),

            "h_index":
                h_index,
            "citation_count": sum(author_citations[author_id])

        })

    return author_metrics