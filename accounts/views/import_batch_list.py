from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from dashboard.models.import_batch import ImportBatch
from django.shortcuts import render



@login_required
def import_batch_list(request):

    if not request.user.roles.filter(name="Admin").exists():
        return HttpResponseForbidden()

    batches = (
        ImportBatch.objects
        .select_related("uploaded_by")
        .order_by("-uploaded_at")
    )

    context = {
        "batches": batches
    }

    return render(
        request,
        "accounts/import_batch_list.html",
        context
    )
