import re

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.http import JsonResponse
from django.shortcuts import render, redirect

from users.models import AuthorLinkRequest
from django.utils import timezone

from users.models import UserProfile


@login_required
def author_link_request_list_view(request):

    status = request.GET.get(

        "status",

        "PENDING"

    )

    queryset = (

        AuthorLinkRequest.objects

        .select_related(

            "user",

            "user__profile__author",

            "author",

            "reviewed_by",

            "reviewed_by__profile"

        )

        .prefetch_related(

            "evidence_publications"

        )

        .order_by(

            "-created_at"

        )

    )

    if status:

        queryset = queryset.filter(

            status=status

        )

    paginator = Paginator(

        queryset,

        20

    )

    page_number = request.GET.get(

        "page"

    )

    page_obj = paginator.get_page(

        page_number

    )

    return render(

        request,

        "accounts/author_link_request_list.html",

        {

            "page_obj": page_obj,

            "status": status

        }

    )


@login_required
def approve_author_link_request(

    request,

    request_id

):
    
    if request.method != "POST":

        return JsonResponse({

            "success": False

        })

    link_request = (

        AuthorLinkRequest.objects

        .select_related(

            "user",

            "author"

        )

        .get(

            id=request_id

        )

    )

    existing_approved = (

        AuthorLinkRequest.objects

        .filter(

            user=link_request.user,

            author=link_request.author,

            status="APPROVED"

        )

        .exclude(

            id=link_request.id

        )

        .exists()

    )

    if existing_approved:

        return JsonResponse({

            "success": False,

            "message":

                "Yêu cầu này đã được duyệt ở một request khác."

        })

    profile, created = (

        UserProfile.objects

        .get_or_create(

            user=link_request.user

        )

    )

    profile.author = (

        link_request.author

    )

    profile.save()

    link_request.status = (

        "APPROVED"

    )

    link_request.reviewed_by = (

        request.user

    )

    link_request.reviewed_at = (

        timezone.now()

    )

    link_request.save()
    # Chuyển trạng thái các yêu cầu của người này bị reject sang cancelled

    AuthorLinkRequest.objects.filter(

        user=link_request.user,

        author=link_request.author

    ).exclude(

        id=link_request.id

    ).update(

        status="CANCELLED"

    )

    return JsonResponse({

        "success": True,

        "status": "APPROVED"

    })


@login_required
def reject_author_link_request(

    request,

    request_id

):

    link_request = (

        AuthorLinkRequest.objects

        .select_related(

            "user",

            "author"

        )

        .get(

            id=request_id

        )

    )

    profile = (

        UserProfile.objects

        .filter(

            user=link_request.user

        )

        .first()

    )

    if (

        profile

        and

        profile.author_id

        ==

        link_request.author_id

    ):

        profile.author = None

        profile.save()

    link_request.status = "REJECTED"

    link_request.reviewed_by = request.user

    link_request.reviewed_at = timezone.now()

    link_request.save()

    return JsonResponse({

        "success": True,
        "status": "REJECTED"

    })


@login_required
def approve_selected_author_link_requests(

    request

):

    ids = request.POST.getlist(

        "request_ids"

    )

    requests = (

        AuthorLinkRequest.objects

        .select_related(

            "user",

            "author"

        )

        .filter(

            id__in=ids,

            status="PENDING"

        )

    )

    for link_request in requests:

        profile = (

            UserProfile.objects.get(

                user=link_request.user

            )

        )

        profile.author = (

            link_request.author

        )

        profile.save()

        link_request.status = (

            "APPROVED"

        )

        link_request.reviewed_by = (

            request.user

        )

        link_request.reviewed_at = (

            timezone.now()

        )

        link_request.save()

    return redirect(

        "author_link_request_list"

    )


def normalize_author_name(name):

    name = name.lower()

    name = re.sub(

        r"[^a-z0-9]",

        "",

        name

    )

    return name


@login_required
def author_link_evidence_api(

    request,

    request_id

):

    link_request = (

        AuthorLinkRequest.objects

        .prefetch_related(

            "evidence_publications__publication_authors__author"

        )

        .get(

            id=request_id

        )

    )

    publications = []

    for publication in (

        link_request.evidence_publications.all()

    ):

        publications.append({

            "title": publication.title,

            "authors": publication.authors_list,

            "year": publication.year,

            "doi": publication.doi

        })

    return JsonResponse({

        "target_author": link_request.author.name,

        "publications": publications

    })