from django.contrib.auth.decorators import (
    login_required
)

from django.http import JsonResponse

from dashboard.models.import_batch import (
    ImportBatch
)


@login_required
def import_progress(request, batch_id):

    try:

        batch = ImportBatch.objects.get(
            id=batch_id
        )

        return JsonResponse({

            "success": True,

            "step": batch.current_step or "Đang xử lý",

            "current": batch.progress_current or 0,

            "total": batch.progress_total or 0,

            "percent": batch.progress_percent or 0,

            "status": batch.status

        })

    except ImportBatch.DoesNotExist:

        return JsonResponse({

            "success": False,

            "message": "Import batch not found"

        }, status=404)

    except Exception as e:

        return JsonResponse({

            "success": False,

            "message": str(e)

        }, status=500)