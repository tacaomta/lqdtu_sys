from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from django.core.paginator import Paginator
from dashboard.models import FactPublication
from django.db.models import (
    Sum
)

from dashboard.services.metrics_service import compute_h_index

@login_required
def my_publications(

    request

):

    profile = getattr(

        request.user,

        "profile",

        None

    )

    author = (

        profile.author

        if profile

        else None

    )

    publications = []

    if author:

        publications = (

            FactPublication.objects

            .filter(

                publication_authors__author=author

            )

            .distinct()

            .order_by(

                "-year",
                "-cited_by"

            )

        )

        paginator = Paginator(

            publications,

            15

        )
        page_number = request.GET.get(

            "page",

            1

        )
        page_obj = paginator.get_page(

            page_number

        )


        citation_count = (

            publications.aggregate(

                total=Sum(

                    "cited_by"

                )

            )["total"]

            or 0

        )

        citation_list = [

            citation or 0

            for citation in publications.values_list(

                "cited_by",

                flat=True

            )

        ]

        h_index = compute_h_index(citation_list)

    return render(

        request,

        "accounts/my_publications.html",

        {

            "author": author,

            "publications": publications,

            "pubs_count": len(publications),

            "citation_count": citation_count,

            "h_index": h_index,

            "page_obj": page_obj

        }

    )