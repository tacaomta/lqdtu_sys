from collections import defaultdict
from collections import Counter
from itertools import combinations
import networkx as nx
from dashboard.models import (
    PublicationAuthor
)
from dashboard.services.collaboration_service import(
    contains_lqdtu,
    contains_vietnam
)
from dashboard.services.metrics_service import compute_publication_h_index
import math

def get_mapping_data(publication_ids):

    # ==========================================
    # BASE QS
    # ==========================================

    publication_affiliation_data = list(

        PublicationAuthor.objects.filter(

            publication_id__in=publication_ids

        )

        .values(

            "publication_id",

            "author_id",

            "author__university__name",

            "author__university__country__name"

        )

    )

    publication_university_country_map = defaultdict(list)

    for row in publication_affiliation_data:

        publication_id = row["publication_id"]

        publication_university_country_map[
            publication_id
        ].append({
            "author_id": row.get("author_id"),

            "university": row.get("author__university__name"),

            "country": row.get("author__university__country__name")

        })

    return publication_university_country_map

def get_collaboration_kpis_info(publication_ids, publication_university_country_map, publication_citation_map):
    '''
    Lấy 13 chỉ số KPIs
    '''
    internal_only_publication_ids = []
    external_collaboration_ids = []
    domestic_collaboration_ids = []
    domestic_authors = set()
    domestic_universities = set()
    international_collaboration_ids = []
    international_authors = set()
    international_universities = set()
    countries = set()

    dos_G = nx.Graph()
    domestic_edge_counter = Counter()
    international_edge_counter = Counter()
    int_G = nx.Graph()


    for publication_id in publication_ids:

        affiliations = publication_university_country_map.get(

            publication_id,

            []

        )
        universities_each_publication = set()
        domestic_universities_each_publication = set()
        international_universities_each_publication = set()
        has_domestic = False
        has_international = False

        for affiliation in affiliations:
            universities_each_publication.add(affiliation["university"])
            if contains_vietnam(affiliation["country"]) and not contains_lqdtu(affiliation["university"]):
           # if contains_vietnam affiliation["country"] == "Viet Nam" and affiliation["university"] != "Le Quy Don Technical University":
                has_domestic = True
                domestic_authors.add(affiliation["author_id"])
                domestic_universities.add(affiliation["university"])
                domestic_universities_each_publication.add(affiliation["university"])


            if not contains_vietnam(affiliation["country"]):
                has_international = True
                international_authors.add(affiliation["author_id"])
                international_universities.add(affiliation["university"])
                countries.add(affiliation["country"])
                international_universities_each_publication.add(affiliation["university"])
        
        if len(universities_each_publication)==1 and contains_lqdtu(list(universities_each_publication)[0]):
            internal_only_publication_ids.append(publication_id)
        else:
            external_collaboration_ids.append(publication_id)
        
        if has_domestic:
            domestic_collaboration_ids.append(publication_id)
            
        if has_international:
            international_collaboration_ids.append(publication_id)

        # Tính network cho domestic
        domestic_universities_each_publication.add("Le Quy Don Technical University")
        domestic_universities_each_publication = list(domestic_universities_each_publication)
        for source, target in combinations(domestic_universities_each_publication, 2):
            if source is None or target is None:
                continue
            edge = tuple(sorted([source, target]))
            domestic_edge_counter[edge] += 1
        # Tính network cho international
        international_universities_each_publication.add("Le Quy Don Technical University")
        international_universities_each_publication = list(international_universities_each_publication)
        for source, target in combinations(international_universities_each_publication, 2):
            if source is None or target is None:
                continue
            edge = tuple(sorted([source, target]))
            international_edge_counter[edge] += 1

    
    # Tính network cho domestic
    for edge, weight in domestic_edge_counter.items():
        source, target = edge
        dos_G.add_edge(source, target, weight=weight)
    domestic_node_sizes = {}
    for node in dos_G.nodes():
        total_weight = sum(dos_G[node][neighbor]["weight"] for neighbor in dos_G.neighbors(node))
        domestic_node_sizes[node] = 25+math.log1p(total_weight) * 12
    domestic_nodes = []
    for node in dos_G.nodes():
        domestic_nodes.append({"data": { "id": node, "label": node, "size": max( 30, domestic_node_sizes[node] * 2 ), "is_lqdtu": 1 if node == "Le Quy Don Technical University" else 0}})
    domestic_edges = [] 
    for source, target, data in dos_G.edges(data=True): 
        domestic_edges.append({ "data": { "source": source, "target": target, "weight": data["weight"] }})
    
    

    # Tính network cho internation
    for edge, weight in international_edge_counter.items():
        source, target = edge
        int_G.add_edge(source, target, weight=weight)
    domestic_node_sizes = {}
    for node in int_G.nodes():
        total_weight = sum(int_G[node][neighbor]["weight"] for neighbor in int_G.neighbors(node))
        domestic_node_sizes[node] = 25+math.log1p(total_weight) * 12
    international_nodes = []
    for node in int_G.nodes():
        international_nodes.append({"data": { "id": node, "label": node, "size": max( 30, domestic_node_sizes[node] * 2 ), "is_lqdtu": 1 if node == "Le Quy Don Technical University" else 0}})
    international_edges = [] 
    for source, target, data in int_G.edges(data=True): 
        international_edges.append({ "data": { "source": source, "target": target, "weight": data["weight"] }})


        
    internal_publication_count = len(internal_only_publication_ids)
    internal_hindex = compute_publication_h_index(internal_only_publication_ids, publication_citation_map)

    external_publication_count = len(external_collaboration_ids)
    external_hindex = compute_publication_h_index(external_collaboration_ids, publication_citation_map)
    

    domestic_publication_count = len(domestic_collaboration_ids)
    domestic_hindex = compute_publication_h_index(domestic_collaboration_ids, publication_citation_map)
    domestic_collaborator_count = len(domestic_authors)
    domestic_partner_university_count = len(domestic_universities)
    
    international_publication_count = len(international_collaboration_ids)
    international_hindex = compute_publication_h_index(international_collaboration_ids, publication_citation_map)
    international_collaborator_count = len(international_authors)
    international_partner_university_count = len(international_universities)
    partner_country_count = len(countries)
    return (
        internal_publication_count,
        internal_hindex,
        external_publication_count,
        external_hindex,
        domestic_publication_count,
        domestic_hindex,
        domestic_collaborator_count,
        domestic_partner_university_count,
        international_publication_count,
        international_hindex,
        international_collaborator_count,
        international_partner_university_count,
        partner_country_count,
        {
            "nodes":domestic_nodes, "edges": domestic_edges
        },
        {
            "nodes":international_nodes, "edges": international_edges
        }
    )









