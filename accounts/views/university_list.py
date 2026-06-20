from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import (
    login_required
)
from dashboard.models.dimensions import University
from django.db.models import Q, Count
from django.core.paginator import Paginator


@login_required
def university_list(request):
    if not (request.user.roles.filter(name="Admin").exists() or request.user.roles.filter(name="Manager").exists()):
        return HttpResponseForbidden()
    return render(request, "accounts/university_list.html")

@login_required
def university_list_api(request):
    keyword = request.GET.get("keyword", "").strip()
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 20))

    queryset = University.objects.select_related("country").distinct().annotate(author_count=Count("authors", distinct=True)).order_by("name")

    if keyword:
        queryset = queryset.filter(
            Q(name__icontains=keyword) |
            Q(country__name__icontains=keyword)
        )

    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)

    records = [{
        "id": u.id,
        "name": u.name,
        "country": u.country.name if u.country else "",
        "author_count": u.author_count
    } for u in page_obj]

    return JsonResponse({
        "records": records,
        "total_records": paginator.count,
        "num_pages": paginator.num_pages,
        "current_page": page_obj.number,
        "has_previous": page_obj.has_previous(),
        "has_next": page_obj.has_next(),
        "start_index": page_obj.start_index(),
        "end_index": page_obj.end_index()
    })
