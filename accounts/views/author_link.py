# accounts/views/author_link.py

from django.http import JsonResponse
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

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

            "publication_authors__author"

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

            for pa in publication.publication_authors.all()

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
def create_author_link_request(request):

    if request.method != "POST":

        return JsonResponse(

            {

                "success": False

            },

            status=405

        )

    payload = json.loads(

        request.body

    )

    author_id = payload.get(

        "author_id"

    )

    publication_ids = payload.get(

        "publication_ids",

        []

    )

    if not author_id:

        return JsonResponse({

            "success": False,

            "message": "Thiếu tác giả."

        })
    
    exists = (

        AuthorLinkRequest.objects

        .filter(

            user=request.user,

            author_id=author_id,

            status="PENDING"

        )

        .exists()

    )

    if exists:

        return JsonResponse({

            "success": False,

            "message":

                "Bạn đã gửi yêu cầu liên kết với tác giả này."

        })

    author = Author.objects.get(

        id=author_id

    )

    link_request = (

        AuthorLinkRequest.objects.create(

            user=request.user,

            author=author,

            status="PENDING"

        )

    )

    publications = (

        FactPublication.objects.filter(

            id__in=publication_ids

        )

    )

    link_request.evidence_publications.set(

        publications

    )

    return JsonResponse({

        "success": True

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


@login_required
def cancel_author_link_request(

    request,

    request_id

):

    if request.method != "POST":

        return JsonResponse({

            "success": False,

            "message": "Invalid request"

        })

    link_request = get_object_or_404(

        AuthorLinkRequest,

        id=request_id,

        user=request.user

    )

    if link_request.status != "PENDING":

        return JsonResponse({

            "success": False,

            "message":

                "Chỉ được hủy yêu cầu đang chờ duyệt."

        })

    link_request.status = "CANCELLED"

    link_request.save()

    return JsonResponse({

        "success": True

    })