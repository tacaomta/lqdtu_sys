from django.contrib.auth.decorators import login_required

from django.db.models import Q

from django.core.paginator import Paginator

from django.http import JsonResponse
from django.shortcuts import render

from dashboard.models import FactPublication

from dashboard.services.cleaners import clean_authors


@login_required
def publication_list(

    request

):

    return render(

        request,

        "dashboard/publication_list.html"

    )



@login_required
def publications_api(

    request

):

    keyword = request.GET.get(

        "keyword",

        ""

    ).strip()

    page_size = int(

        request.GET.get(

            "page_size",

            10

        )

    )

    page = int(

        request.GET.get(

            "page",

            1

        )

    )

    year = request.GET.get(

        "year",

        ""

    ).strip()

    document_type = request.GET.get(

        "document_type",

        ""

    ).strip()

    queryset = (

        FactPublication.objects

        .all()

    )

    if keyword:

        queryset = (

            queryset.filter(

                Q(title__icontains=keyword)

                |

                Q(authors_list__icontains=keyword)

            )

        )

    if year:

        queryset = queryset.filter(

            year=year

        )

    if document_type:

        queryset = queryset.filter(

            document_type=document_type

        )

    paginator = Paginator(

        queryset,

        page_size

    )

    page_obj = paginator.get_page(

        page

    )

    results = []

    for publication in page_obj:

        results.append({

            "id": publication.id,

            "year": publication.year,

            "title": publication.title,

            "authors":

                clean_authors(

                    publication.authors_list

                ),

            "citation":

                publication.cited_by,

            "doi":

                publication.doi,

            "document_type":

                publication.document_type,
            "journal": publication.journal

        })

    return JsonResponse({

    "records": results,

    "total_count":

        paginator.count,

    "current_page":

        page_obj.number,

    "num_pages":

        paginator.num_pages,

    "has_next":

        page_obj.has_next(),

    "has_previous": page_obj.has_previous(),

    "start_index": page_obj.start_index(),

    "end_index": page_obj.end_index()

})


@login_required
def publication_filter_options_api(

    request

):

    years = list(

        FactPublication.objects

        .exclude(

            year__isnull=True

        )

        .values_list(

            "year",

            flat=True

        )

        .distinct()

        .order_by(

            "-year"

        )

    )

    document_types = list(

        FactPublication.objects

        .exclude(

            document_type__isnull=True

        )

        .exclude(

            document_type=""

        )

        .values_list(

            "document_type",

            flat=True

        )

        .distinct()

        .order_by(

            "document_type"

        )

    )

    return JsonResponse({

        "years": years,

        "document_types": document_types

    })