import json
from pathlib import Path

from django.contrib.auth.decorators import (
    login_required
)

from django.shortcuts import render

from django.http import JsonResponse

from dashboard.forms import (
    UploadCSVForm
)

from dashboard.services.importer import (
    import_publications
)
from dashboard.services.file_validation import file_validate

from dashboard.models.raw import (
    PublicationRaw
)


from dashboard.models import ImportBatch

import threading

from dashboard.services.config_service import is_dirty


# =========================================================
# UPLOAD CSV / EXCEL
# =========================================================

@login_required
def upload_csv(request):

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        form = UploadCSVForm(

            request.POST,

            request.FILES

        )

        # =================================================
        # INVALID FORM
        # =================================================

        if not form.is_valid():

            return JsonResponse({

                "success": False,

                "message": (
                    "Form upload không hợp lệ."
                )

            }, status=400)

        try:

            # =============================================
            # FILE
            # =============================================

            file = request.FILES["file"]

            extension = (

                Path(

                    file.name

                )

                .suffix

                .lower()

            )
            allowed_extensions = {".csv", ".xlsx", ".xls"}
            if extension not in allowed_extensions:
                return JsonResponse({

                "success": False,

                "message": "Lỗi định dạng file"

            })


            # validated here
            valid, message, required_columns = file_validate(file, extension)
            if not valid:
                return JsonResponse({

                "success": False,

                "message": message,
                "required_columns": list(required_columns)

            })

            batch = ImportBatch.objects.create( filename=file.name, uploaded_file = file, status="PROCESSING", uploaded_by_id=request.user.id, 
                                               data_updated_until=request.POST.get("data_updated_until")
                                               )

            threading.Thread( target=import_publications, args=(batch.id, ), daemon=True ).start()

            # =============================================
            # JSON RESPONSE
            # =============================================

            return JsonResponse({

                "success": True,

                "batch_id": batch.id,

                "status": "PROCESSING"

            })

        # =================================================
        # ERROR
        # =================================================

        except Exception as e:

            return JsonResponse({

                "success": False,

                "message": str(e)

            }, status=500)

    # =====================================================
    # GET
    # =====================================================

    form = UploadCSVForm()


    latest_batch = ImportBatch.objects.order_by(
        "-id"
    ).first()

    result = None

    if latest_batch:

        preview_qs = (
            PublicationRaw.objects
            .filter(import_batch=latest_batch)
            .order_by("id")
        )

        # =========================================
        # PREVIEW COLUMNS
        # =========================================

        preview_columns = [

            "title",

            "year",

            "doi",

            "author_affiliations",

            "field",

            "subfield"

        ]

        # =========================================
        # HEAD
        # =========================================

        preview_head = list(

            preview_qs
            .values(*preview_columns)[:5]

        )

        # =========================================
        # TAIL
        # =========================================

        preview_tail = list(

            preview_qs
            .values(*preview_columns)
            .reverse()[:5]

        )

        preview_tail.reverse()

        # =========================================
        # RESULT
        # =========================================

        result = {

            "total_rows":
                latest_batch.total_rows,

            "valid_rows":
                latest_batch.total_rows
                - latest_batch.duplicated_count,

            "duplicates":
                latest_batch.duplicated_count,

            "missing_doi":
                latest_batch.doi_missing_count,

            "inserted":
                latest_batch.inserted_count,

            "updated":
                latest_batch.updated_count,
            
            "existing_doi":
                latest_batch.existing_doi_count,
            
            "new_doi":
                latest_batch.new_doi_count,

            "enriched_success":
                latest_batch.enriched_success,
            
            "enriched_failed":
                latest_batch.enriched_failed,

            "preview_head":
                preview_head,

            "preview_tail":
                preview_tail,

            "preview_columns":
                preview_columns,

            "data_updated_until": latest_batch.data_updated_until,

            "logs": [

                # =====================================
                # STEP 1
                # =====================================

                "BƯỚC 1 — Bắt đầu đọc file dữ liệu",

                f"Đọc thành công {latest_batch.total_rows} bản ghi",

                # =====================================
                # STEP 2
                # =====================================

                "BƯỚC 2 — Tiền xử lý dữ liệu",

                ("Chuẩn hóa các trường dữ liệu quan trọng"),

                (
                    f"Loại bỏ "
                    f"{latest_batch.duplicated_count} "
                    f"bản ghi trùng lặp"
                ),

                (
                    f"Dữ liệu hợp lệ còn lại: "
                    f"{latest_batch.total_rows - latest_batch.duplicated_count}"
                ),

                # =====================================
                # STEP 3
                # =====================================

                "BƯỚC 3 — Cập nhật thông tin ngành, chuyên ngành",

                (
                    f"Bỏ qua "
                    f"{latest_batch.doi_missing_count} "
                    f"bản ghi thiếu DOI"
                ),

                (
                    f"Có "
                    f"{latest_batch.existing_doi_count} "
                    f"bản ghi đã tồn tại trong CSDL"
                ),

                (
                    f"Cập nhật "
                    f"{latest_batch.updated_count} "
                    f"bản ghi có DOI tồn tại nhưng cập nhật thông tin về Citation"
                ),

                (
                    f"Có "
                    f"{latest_batch.new_doi_count} "
                    f"bản ghi có DOI mới"
                ),

                (
                    f"Thêm mới "
                    f"{latest_batch.inserted_count} "
                    f"DOI mới"
                ),

                (
                    f"Lấy chuyên ngành thành công: "
                    f"{latest_batch.enriched_success}"
                ),

                (
                    f"Không xác định được chuyên ngành: "
                    f"{latest_batch.enriched_failed}"
                ),                
                
                # =====================================
                # STEP 4
                # =====================================

                "BƯỚC 4 — Lưu dữ liệu vào hệ thống",

                (
                    f"Hoàn tất lưu "
                    f"{latest_batch.inserted_count} và cập nhật  {latest_batch.updated_count}"
                    f"bản ghi"
                ),

                "Quá trình đọc, xử lý, lưu dữ liệu hoàn tất"

            ]
        }


    # =====================================================
    # RENDER
    # =====================================================

    return render(

        request,

        "dashboard/upload.html",

        {

            "form": form,

            "result": result,

            "config_dirty": is_dirty(),

        }

    )