from django.shortcuts import render

from django.contrib.auth import get_user_model

from accounts.forms.register_form import RegisterForm

from users.models import UserProfile, Role

User = get_user_model()


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(

            request.POST

        )

        if form.is_valid():

            user = User.objects.create_user(

                username=form.cleaned_data["username"],

                email=form.cleaned_data["email"],

                password=form.cleaned_data["password1"]

            )

            UserProfile.objects.create(

                user=user,

                fullname=form.cleaned_data["fullname"]

            )
            author_role = Role.objects.get(

                name="AUTHOR"

            )

            user.roles.add(author_role)

            success_message = (
            "Đăng ký tài khoản thành công. "
            "Bạn có thể chuyển sang trang đăng nhập."
            )

            form = RegisterForm()

            return render(

                request,

                "accounts/register.html",

                {

                    "form": form,

                    "success_message": success_message

                }

            )

    else:

        form = RegisterForm()

    return render(

        request,

        "accounts/register.html",

        {

            "form": form

        }

    )