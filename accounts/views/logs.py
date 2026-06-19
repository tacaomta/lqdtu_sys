from django.contrib.auth.decorators import (
    login_required
)

from django.shortcuts import render

from users.models import LoginLog
from django.http import HttpResponseForbidden, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime


@login_required
def login_log_list(request):

    if not request.user.roles.filter(
        name="Admin"
    ).exists():

        return HttpResponseForbidden()

    return render(

        request,

        "accounts/login_logs.html"

    )


@login_required
def delete_login_log(

    request,

    log_id

):

    if not request.user.roles.filter(
        name="Admin"
    ).exists():

        return JsonResponse(
            {
                "success": False
            },
            status=403
        )

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False
            },
            status=400
        )

    LoginLog.objects.filter(
        id=log_id
    ).delete()

    return JsonResponse(
        {
            "success": True
        }
    )


@login_required
def clear_login_logs(request):

    if not request.user.roles.filter(
        name="Admin"
    ).exists():

        return JsonResponse(
            {
                "success": False
            },
            status=403
        )

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False
            },
            status=400
        )

    LoginLog.objects.all().delete()

    return JsonResponse(
        {
            "success": True
        }
    )


@login_required
def login_log_api(request):

    if not request.user.roles.filter(
        name="Admin"
    ).exists():

        return JsonResponse(
            {"success": False},
            status=403
        )

    page = int(
        request.GET.get(
            "page",
            1
        )
    )

    page_size = int(
        request.GET.get(
            "page_size",
            10
        )
    )

    keyword = (
        request.GET.get(
            "keyword",
            ""
        )
        .strip()
    )

    start_date = (
        request.GET.get(
            "start_date",
            ""
        )
        .strip()
    )

    end_date = (
        request.GET.get(
            "end_date",
            ""
        )
        .strip()
    )

    queryset = LoginLog.objects.all()
    if keyword:

        queryset = queryset.filter(

            Q(
                username__icontains=keyword
            )

            |

            Q(
                fullname__icontains=keyword
            )

        )

    if start_date:
        queryset = queryset.filter(
            login_time__date__gte=
            start_date
        )

    if end_date:
        queryset = queryset.filter(
            login_time__date__lte=
            end_date
        )

    paginator = Paginator(
        queryset,
        page_size
    )

    page_obj = paginator.get_page(
        page
    )

    records = []

    for log in page_obj:

        records.append({

            "id": log.id,

            "username":
                log.username,

            "fullname":
                log.fullname,

            "login_time":
                log.login_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "logout_time":
                (
                    log.logout_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if log.logout_time
                    else None
                ),

            "ip_address":
                log.ip_address,

            "user_agent":
                log.user_agent

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