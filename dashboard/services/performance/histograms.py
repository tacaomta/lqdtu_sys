def get_author_histograms(author_metrics):

    publication_bins = [

        "1",
        "2-3",
        "4-5",
        "6-10",
        "11-20",
        ">20"

    ]

    citation_bins = [
        "0",
        "1-49",
        "50-99",
        "100-199",
        "200-499",
        "500-999",
        "1000+"
    ]

    publication_bin_counts = [

        0, 0, 0, 0, 0, 0

    ]


    # ==========================================
    # HISTOGRAM - CITATION GROUP
    # ==========================================

    citation_bin_counts = {group: 0 for group in citation_bins}

    # ==========================================
    # LOOP AUTHORS
    # ==========================================

    for author_metric in author_metrics:

        publication_count = author_metric[
            "publication_count"
        ]

        citation_count = author_metric[
            "citation_count"
        ]


        # =====================================
        # PUBLICATION BIN
        # =====================================

        if publication_count == 1:

            publication_bin_counts[0] += 1

        elif 2 <= publication_count <= 3:

            publication_bin_counts[1] += 1

        elif 4 <= publication_count <= 5:

            publication_bin_counts[2] += 1

        elif 6 <= publication_count <= 10:

            publication_bin_counts[3] += 1

        elif 11 <= publication_count <= 20:

            publication_bin_counts[4] += 1

        else:

            publication_bin_counts[5] += 1


        # =====================================
        # CITATION BIN
        # =====================================

        if citation_count == 0:

            group = "0"

        elif 1 <= citation_count and citation_count <= 49:

           group = "1-49"

        elif 50 <= citation_count and citation_count <= 99:

            group = "50-99"

        elif 100 <= citation_count and citation_count <= 199:

            group = "100-199"

        elif 200 <= citation_count and citation_count <= 499:

            group = "200-499"
        elif 500 <= citation_count and citation_count <= 999:
            group = "500-999"

        else:

            group = "1000+"
        
        citation_bin_counts[group] += 1 

        citation_bin_values = [citation_bin_counts[i] for i in citation_bins]

    return publication_bins, publication_bin_counts, citation_bins, citation_bin_values