from django.contrib.auth.decorators import (
    login_required
)
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse

from dashboard.models.dimensions import Author

@login_required
def author_list(request):

    if not (

        request.user.roles.filter(
            name="Admin"
        ).exists()

        or

        request.user.roles.filter(
            name="Manager"
        ).exists()

    ):

        return HttpResponseForbidden()

    return render(

        request,

        "accounts/author_list.html"

    )

@login_required
def author_list_api(request):

    keyword = request.GET.get(
        "keyword",
        ""
    ).strip()

    page = int(
        request.GET.get(
            "page",
            1
        )
    )

    page_size = int(
        request.GET.get(
            "page_size",
            20
        )
    )

    queryset = (

        Author.objects

        .select_related(
            "university"
        )

        .order_by(
            "name"
        )

    )
    if keyword:

        queryset = queryset.filter(

            Q(
                name__icontains=keyword
            )

            |

            Q(
                university__name__icontains=keyword
            )

            |

            Q(
                university__country__name__icontains=keyword
            )

        )
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    records = []

    for author in page_obj:

        records.append({

            "id":
                author.id,

            "name":
                author.name,

            "university":

                author.university.name

                if author.university

                else "",

            "country":

                author.university.country.name

                if (

                    author.university

                    and

                    author.university.country

                )

                else ""

        })
    return JsonResponse({

        "records":
            records,

        "total_records":
            paginator.count,

        "num_pages":
            paginator.num_pages,

        "current_page":
            page_obj.number,

        "has_previous":
            page_obj.has_previous(),

        "has_next":
            page_obj.has_next(),
        "start_index": page_obj.start_index(),
        "end_index": page_obj.end_index()

    })