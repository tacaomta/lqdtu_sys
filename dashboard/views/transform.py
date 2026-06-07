from django.contrib.auth.decorators import (
    login_required
)

from django.shortcuts import render

from django.http import JsonResponse

from django.views.decorators.http import (
    require_POST
)

from dashboard.models import (
    PublicationRaw,
    FactPublication
)

from dashboard.services.transformers import (
    transform_publications
)

from dashboard.services.config_service import is_dirty


# =========================================================
# TRANSFORM DASHBOARD
# =========================================================

@login_required
def transform_dashboard(request):

    # =====================================================
    # RAW STATS
    # =====================================================

    total_raw = (
        PublicationRaw.objects.count()
    )

    processed_raw = (
        PublicationRaw.objects.filter(
            processed=True
        ).count()
    )

    pending_raw = (
        PublicationRaw.objects.filter(
            processed=False
        ).count()
    )

    # =====================================================
    # FACT STATS
    # =====================================================

    total_fact = (
        FactPublication.objects.count()
    )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {
        "config_dirty": is_dirty(),

        "total_raw": total_raw,

        "processed_raw": processed_raw,

        "pending_raw": pending_raw,

        "total_fact": total_fact,

        "inserted_count": 0,

        "updated_count": 0

    }

    return render(

        request,

        "dashboard/transform.html",

        context

    )


# =========================================================
# RUN TRANSFORMATION
# =========================================================

@login_required
@require_POST
def transform_data(request):

    try:

        # =================================================
        # FORCE REBUILD OPTION
        # =================================================

        force_rebuild = (

            request.POST.get(
                "force_rebuild"
            ) == "true"

        )

        # =================================================
        # RUN TRANSFORM
        # =================================================

        result = transform_publications(

            force_rebuild=force_rebuild

        )

        # =================================================
        # SUCCESS RESPONSE
        # =================================================

        # =================================================
        # REFRESH DASHBOARD STATS
        # =================================================

        total_raw = (
            PublicationRaw.objects.count()
        )

        processed_raw = (
            PublicationRaw.objects.filter(
                processed=True
            ).count()
        )

        pending_raw = (
            PublicationRaw.objects.filter(
                processed=False
            ).count()
        )

        total_fact = (
            FactPublication.objects.count()
        )

        # =================================================
        # RESPONSE
        # =================================================

        return JsonResponse({

            "success": True,

            # =============================================
            # TRANSFORM RESULT
            # =============================================

            "processed_count": result.get(
                "processed_count",
                0
            ),

            "inserted_count": result.get(
                "inserted_count",
                0
            ),

            "updated_count": result.get(
                "updated_count",
                0
            ),

            # =============================================
            # DASHBOARD STATS
            # =============================================

            "total_raw": total_raw,

            "processed_raw": processed_raw,

            "pending_raw": pending_raw,

            "total_fact": total_fact,

            # =============================================
            # MESSAGE
            # =============================================

            "message": result.get(
                "message",
                "Transformation completed."
            )

        })



    except Exception as e:

        return JsonResponse({

            "success": False,

            "message": str(e)

        }, status=500)