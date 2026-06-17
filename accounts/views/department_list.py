from django.contrib.auth.decorators import login_required
from users.models import Department, UserProfile
from django.shortcuts import render
from django.http import JsonResponse


@login_required
def department_list(request):

    departments = Department.objects.order_by("name")

    context = {
        "departments": departments
    }

    return render(
        request,
        "accounts/department_list.html",
        context
    )


@login_required
def create_department(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "message": "Phương thức không hợp lệ"
            },
            status=400
        )

    name = request.POST.get(
        "name",
        ""
    ).strip()

    if not name:

        return JsonResponse(
            {
                "success": False,
                "message": "Tên Department không được để trống"
            }
        )

    if Department.objects.filter(
        name__iexact=name
    ).exists():

        return JsonResponse(
            {
                "success": False,
                "message": "Department đã tồn tại"
            }
        )

    department = Department.objects.create(
        name=name
    )

    return JsonResponse(
        {
            "success": True,
            "message": "Tạo Department thành công",
            "id": department.id,
            "name": department.name
        }
    )


@login_required
def update_department(request, department_id):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "message": "Phương thức không hợp lệ"
            },
            status=400
        )

    department = Department.objects.get(
        id=department_id
    )

    name = request.POST.get(
        "name",
        ""
    ).strip()

    if not name:

        return JsonResponse(
            {
                "success": False,
                "message": "Tên Department không được để trống"
            }
        )

    duplicated = Department.objects.exclude(
        id=department.id
    ).filter(
        name__iexact=name
    ).exists()

    if duplicated:

        return JsonResponse(
            {
                "success": False,
                "message": "Department đã tồn tại"
            }
        )

    department.name = name

    department.save()

    return JsonResponse(
        {
            "success": True,
            "message": "Cập nhật Department thành công"
        }
    )

@login_required
def delete_department(request, department_id):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "message": "Phương thức không hợp lệ"
            },
            status=400
        )

    department = Department.objects.get(
        id=department_id
    )

    in_use = UserProfile.objects.filter(
        department=department
    ).exists()

    if in_use:

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "Không thể xóa Department vì đang được sử dụng."
                )
            }
        )

    department.delete()

    return JsonResponse(
        {
            "success": True,
            "message": "Xóa Department thành công"
        }
    )