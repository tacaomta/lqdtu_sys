# ==========================================
# COMPUTE H-INDEX
# ==========================================

def compute_h_index(citations):

    citations = sorted(

        citations,

        reverse=True

    )

    h = 0

    for i, c in enumerate(

        citations,

        start=1

    ):

        if c >= i:

            h = i

        else:

            break

    return h

def compute_publication_h_index(publication_ids, publication_citation_map):

    citations = [publication_citation_map.get(i, 0) for i in publication_ids]

    return compute_h_index(

        citations

    )