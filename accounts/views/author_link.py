# accounts/views/author_link.py

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.models.dimensions import Author
from dashboard.models.fact import FactPublication
from users.models import AuthorLinkRequest

@login_required
def author_search_api(request):

    q = request.GET.get(

        "q",

        ""

    )

    authors = (

        Author.objects

        .filter(

            university__name="Le Quy Don Technical University",

            name__icontains=q

        )

        .order_by("name")[:20]

    )

    return JsonResponse({

        "results": [

            {

                "id": author.id,

                "text": author.name

            }

            for author in authors

        ]

    })

@login_required
def publication_search_api(request):

    q = request.GET.get(

        "q",

        ""

    ).strip()

    publications = (

        FactPublication.objects

        .filter(

            title__icontains=q

        )

        .prefetch_related(

            "publicationauthor_set__author"

        )

        .only(

            "id",

            "title",

            "year",

            "doi"

        )

        [:20]

    )

    results = []

    for publication in publications:

        authors = [

            pa.author.name

            for pa in publication.publicationauthor_set.all()

        ]

        results.append({

            "id": publication.id,

            "title": publication.title,

            "authors": "; ".join(authors),

            "year": publication.year,

            "doi": publication.doi,

            "text": (

                f"{publication.title[:120]} "

                f"({publication.year})"

            )

        })

    return JsonResponse({

        "results": results

    })


@login_required
def author_link_view(request):

    requests = (

        AuthorLinkRequest.objects

        .filter(

            user=request.user

        )

        .select_related(

            "author"

        )

        .order_by(

            "-created_at"

        )

    )

    return render(

        request,

        "accounts/author_link.html",

        {

            "requests": requests

        }

    )