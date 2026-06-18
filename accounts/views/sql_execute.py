from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import re
from django.db import connection
from django.http import JsonResponse


@login_required
def sql_execute_view(request):

    context = {}

    return render(
        request,
        "accounts/sql_execute.html",
        context
    )


@login_required
def execute_sql(request):

    if not request.user.roles.filter(
        name="Admin"
    ).exists():

        return JsonResponse(
            {
                "success": False,
                "message": "Không có quyền truy cập"
            },
            status=403
        )

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "message": "Phương thức không hợp lệ"
            },
            status=400
        )

    sql_text = request.POST.get(
        "sql",
        ""
    ).strip()

    if not sql_text:

        return JsonResponse(
            {
                "success": False,
                "message": "SQL không được để trống"
            }
        )

    normalized_sql = re.sub(
        r"\s+",
        " ",
        sql_text
    ).upper()

    if not (
        normalized_sql.startswith("UPDATE ")
        or
        normalized_sql.startswith("INSERT ")
    ):

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "Chỉ cho phép UPDATE hoặc INSERT"
                )
            }
        )
    
    if ";" in sql_text:

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "Không cho phép thực thi nhiều câu lệnh cùng lúc"
                )
            }
        )

    blocked_keywords = [

        "DROP ",
        "TRUNCATE ",
        "ALTER ",
        "CREATE ",
        "DELETE ",
        "MERGE ",
        "EXEC ",
        "XP_",
        "SP_",
        "BACKUP ",
        "RESTORE ",
        "SHUTDOWN ",
        "SELECT "

    ]

    for keyword in blocked_keywords:

        if keyword in normalized_sql:

            return JsonResponse(
                {
                    "success": False,
                    "message": (
                        f"Câu lệnh chứa từ khóa bị cấm: {keyword.strip()}"
                    )
                }
            )

    try:

        with connection.cursor() as cursor:

            cursor.execute(sql_text)

            affected_rows = cursor.rowcount

        return JsonResponse(
            {
                "success": True,
                "message": (
                    f"Thực thi thành công "
                    f"({affected_rows} dòng bị ảnh hưởng)"
                )
            }
        )

    except Exception as ex:

        return JsonResponse(
            {
                "success": False,
                "message": str(ex)
            }
        )