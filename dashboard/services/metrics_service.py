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