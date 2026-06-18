from django.shortcuts import render


def test_view(request):
    return render(

        request,

        "base_v2.html",
        {"dashboard_active": True}

    )