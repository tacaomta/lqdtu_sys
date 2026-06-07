from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from users.models import UserProfile
from accounts.forms.user_profile_form import ProfileForm


@login_required
def profile_view(request):

    profile, _ = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Cập nhật hồ sơ thành công."
            )

            return redirect(
                "profile"
            )

    else:

        form = ProfileForm(
            instance=profile
        )

    roles = ", ".join(

        request.user.roles.values_list(

            "name",

            flat=True

        )

    )

    return render(

        request,

        "accounts/profile.html",

        {

            "form": form,

            "profile": profile,

            "roles": roles

        }

    )