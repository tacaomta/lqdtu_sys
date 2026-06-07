from django.contrib import messages

from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from accounts.forms.change_password_form import (
    ChangePasswordForm
)


@login_required
def change_password_view(request):

    form = ChangePasswordForm(

        request.POST or None

    )

    if request.method == "POST":

        if form.is_valid():

            current_password = form.cleaned_data[

                "current_password"

            ]

            new_password = form.cleaned_data[

                "new_password"

            ]

            if not request.user.check_password(

                current_password

            ):

                form.add_error(

                    "current_password",

                    "Mật khẩu hiện tại không chính xác."

                )

            else:

                request.user.set_password(

                    new_password

                )

                request.user.save()

                update_session_auth_hash(

                    request,

                    request.user

                )

                messages.success(

                    request,

                    "Đổi mật khẩu thành công."

                )

    return render(

        request,

        "accounts/change_password.html",

        {

            "form": form

        }

    )