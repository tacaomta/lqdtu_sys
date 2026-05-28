from collections import Counter
from dashboard.models import (
    FactPublication
)
from dashboard.services.metrics_service import compute_publication_h_index


def get_list_info_each_affiliation(affiliations):

    universities_set = set()

    domestic_universities = set()

    international_universities = set()

    countries = set()
    for affiliation in affiliations:

        university = affiliation["university"]

        country = affiliation["country"]
        universities_set.add(university)


        if not university:
            continue


        # =================================
        # DOMESTIC UNIVERSITY
        # =================================

        if (
            country == "Viet Nam"
            and
            university != "Le Quy Don Technical University"
        ):

            domestic_universities.add(
                university
            )


        # =================================
        # INTERNATIONAL UNIVERSITY
        # =================================

        elif country != "Viet Nam":

            international_universities.add(
                university
            )


        # =================================
        # COUNTRIES
        # =================================

        if country != "Viet Nam":

            countries.add(
                country
            )
        
    if universities_set == {"Le Quy Don Technical University"}:
        internal = True
    else:
        internal = False
    
    return internal, domestic_universities, international_universities, countries


def get_field_collaboration_chart_data(qs, FIELD_GROUP_ORDER, publication_university_country_map, publication_citation_map):
    """
    Chuẩn bị dữ liệu
    """
    domestic_university_counter = Counter()

    international_university_counter = Counter()

    country_counter = Counter()

    internal_counts = []

    external_counts = []

    internal_hindexes = []

    external_hindexes = []

    domestic_counts = []

    international_counts = []

    domestic_hindexes = []

    international_hindexes = []

    for field_group in FIELD_GROUP_ORDER:

        field_qs = qs.filter(

            field_group=field_group

        )


        publication_ids = list(

            field_qs.values_list(

                "id",

                flat=True

            )

        )


        internal_ids = []

        external_ids = []
        domestic_ids = []
        international_ids = []


        for publication_id in publication_ids:

            affiliations = publication_university_country_map.get(

                publication_id,

                []

            )

            internal, domestic_universities, international_universities, countries =get_list_info_each_affiliation(affiliations)
            for university in domestic_universities:

                domestic_university_counter[
                    university
                ] += 1


            for university in international_universities:

                international_university_counter[
                    university
                ] += 1


            for country in countries:

                country_counter[
                    country
                ] += 1


            # =====================================
            # INTERNAL
            # =====================================

            if internal:
                internal_ids.append(

                    publication_id

                )
            # =====================================
            # EXTERNAL
            # =====================================

            else:

                external_ids.append(

                    publication_id

                )

            if len(domestic_universities)>0:
                domestic_ids.append(publication_id)
            if len(international_universities)>0:
                international_ids.append(publication_id)

        # Dữ liệu top N xếp từ cao đến thấp
        domestic_university_ranking = [

        {
            "name": name,
            "count": count
        }

        for name, count
        in domestic_university_counter.most_common()
        ]

        international_university_ranking = [

            {
                "name": name,
                "count": count
            }

            for name, count
            in international_university_counter.most_common()
        ]


        country_ranking = [
            {
                "name": name,
                "count": count
            }
            for name, count
            in country_counter.most_common()
        ]



        # =====================================
        # H-INDEX
        # =====================================

        internal_hindex = compute_publication_h_index(internal_ids, publication_citation_map)
        external_hindex = compute_publication_h_index(external_ids, publication_citation_map)
        domestic_hindex = compute_publication_h_index(domestic_ids, publication_citation_map)
        international_hindex = compute_publication_h_index(international_ids, publication_citation_map)



        # =====================================
        # APPEND
        # =====================================

        internal_counts.append(len(internal_ids))
        external_counts.append(len(external_ids))
        internal_hindexes.append(internal_hindex)
        external_hindexes.append(external_hindex)

        domestic_counts.append(len(domestic_ids))
        international_counts.append(len(international_ids))
        domestic_hindexes.append(domestic_hindex)
        international_hindexes.append(international_hindex)

    field_collaboration_in_ex_datasets = [

        {

            "label":
                "Chỉ LQDTU",

            "data":
                internal_counts

        },

        {

            "label":
                "Hợp tác bên ngoài",

            "data":
                external_counts

        }

    ]

    domestic_international_datasets = [

        {

            "label":
                "Hợp tác trong nước",

            "data":
                domestic_counts

        },

        {

            "label":
                "Hợp tác quốc tế",

            "data":
                international_counts

        }

    ]

    field_in_ex_hindex_datasets = [

        {

            "label":
                "Chỉ LQDTU",

            "data":
                internal_hindexes

        },

        {

            "label":
                "Hợp tác ngoài",

            "data":
                external_hindexes

        }

    ]

    domestic_international_hindex_datasets = [

        {

            "label":
                "Hợp tác trong nước",

            "data":
                domestic_hindexes

        },

        {

            "label":
                "Hợp tác quốc tế",

            "data":
                international_hindexes

        }

    ]


    return (field_collaboration_in_ex_datasets, 
            field_in_ex_hindex_datasets, 
            domestic_international_datasets, 
            domestic_international_hindex_datasets,
            domestic_university_ranking,
            international_university_ranking,
            country_ranking)





