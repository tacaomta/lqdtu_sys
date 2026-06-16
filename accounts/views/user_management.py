# accounts/views/user_management.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from users.models import Department, User, AuthorLinkRequest, UserProfile, Role

from django.core.paginator import Paginator

from django.db.models import Q, Prefetch

from django.shortcuts import render, redirect

from django.contrib import messages


@login_required
def user_list(

    request

):

    keyword = (

        request.GET.get(

            "keyword",

            ""

        ).strip()

    )

    queryset = (

        User.objects

        .select_related(

            "profile"

        )

        .prefetch_related(

            "roles",
            Prefetch(

                "authorlinkrequest_set",

                queryset=

                    AuthorLinkRequest.objects.filter(

                        status="APPROVED"

                    ).select_related(

                        "author"

                    ),to_attr="approved_author_links"

                )
        )

        .order_by(

            "username"

        )

    )

    if keyword:

        queryset = (

            queryset.filter(

                Q(

                    username__icontains=keyword

                )

                |

                Q(

                    email__icontains=keyword

                )

                |

                Q(

                    profile__full_name__icontains=keyword

                )

            )

        )

    paginator = Paginator(

        queryset,

        20

    )

    page_number = (

        request.GET.get(

            "page"

        )

    )

    page_obj = (

        paginator.get_page(

            page_number

        )

    )

    context = {

        "page_obj": page_obj,

        "keyword": keyword

    }

    return render(

        request,

        "accounts/user_list.html",

        context

    )



@login_required
def toggle_user_status(

    request,

    user_id

):

    if request.method != "POST":

        return JsonResponse(

            {

                "success": False

            },

            status=405

        )

    target_user = (

        User.objects.get(

            id=user_id

        )

    )

    # không cho tự block chính mình

    if target_user == request.user:

        return JsonResponse({

            "success": False,

            "message":

                "Không thể khóa chính tài khoản đang đăng nhập"

        })

    target_user.is_active = (

        not target_user.is_active

    )

    target_user.save()

    return JsonResponse({

        "success": True,

        "is_active":

            target_user.is_active

    })


@login_required
def create_user(

    request

):
    
    User = get_user_model()

    roles = (

        Role.objects.all()

        .order_by(

            "name"

        )

    )

    if request.method == "POST":

        username = (

            request.POST.get(

                "username",

                ""

            ).strip()

        )

        email = (

            request.POST.get(

                "email",

                ""

            ).strip()

        )

        password = (

            request.POST.get(

                "password",

                ""

            )

        )

        role_ids = (

            request.POST.getlist(

                "role_id"

            )

        )

        fullname = (

            request.POST.get(

                "fullname",

                ""

            ).strip()

        )

        department_id = request.POST.get("department_id")
        department = None

        if department_id:

            department = (

                Department.objects.get(

                    id=department_id

                )

            )

        if not username:

            messages.error(

                request,

                "Tên đăng nhập không được để trống"

            )

        elif not password:

            messages.error(

                request,

                "Mật khẩu không được để trống"

            )
        elif len(password)<8:
            messages.error(

                request,

                "Mật khẩu phải chứa ít nhất 8 ký tự"

            )
        elif email and User.objects.filter(email=email).exists():
            messages.error(
                request, "Email đã tồn tại"
            )

        elif User.objects.filter(

            username=username

        ).exists():

            messages.error(

                request,

                "Tên đăng nhập đã tồn tại"

            )

        else:

            user = (

                User.objects.create_user(

                    username=username,

                    email=email,

                    password=password

                )

            )

            if role_ids:

                user.roles.set(

                    Role.objects.filter(id__in = role_ids)

                )

            UserProfile.objects.create(

                user=user,

                fullname=fullname,

                department=department

            )

            messages.success(

                request,

                "Tạo tài khoản thành công"

            )

            return redirect(

                "user_list"

            )
    departments = (

        Department.objects

        .order_by(

            "name"

        )

    )

    context = {

        "roles": roles,
        "departments": departments

    }

    return render(

        request,

        "accounts/create_user_form.html",

        context

    )