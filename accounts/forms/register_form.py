from django import forms

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.Form):

    username = forms.CharField(

        max_length=150,

        label="Tên đăng nhập",

        required=True,
        error_messages={"required": "Vui lòng nhập tên đăng nhập"}

    )

    fullname = forms.CharField(

        max_length=255,

        label="Họ và tên",
        required=False

    )

    email = forms.EmailField(

        label="Email",
        required=True,
        error_messages={"required": "Vui lòng nhập email"}

    )

    password1 = forms.CharField(

        widget=forms.PasswordInput,

        label="Mật khẩu",
        required=True,
        error_messages={"required": "Vui lòng nhập mật khẩu"}

    )

    password2 = forms.CharField(

        widget=forms.PasswordInput,

        label="Xác nhận mật khẩu",
        required=True,
        error_messages={"required": "Vui lòng nhắc lại mật khẩu"}

    )

    def clean_username(self):

        username = self.cleaned_data["username"].strip()

        if len(username) < 6:

            raise forms.ValidationError(
                "Tên đăng nhập phải có ít nhất 6 ký tự."
            )

        if " " in username:

            raise forms.ValidationError(
                "Tên đăng nhập không được chứa khoảng trắng."
            )

        if username.isdigit():

            raise forms.ValidationError(
                "Tên đăng nhập không được chỉ gồm số."
            )

        if User.objects.filter(
            username=username
        ).exists():

            raise forms.ValidationError(
                "Tên đăng nhập đã tồn tại."
            )

        return username

    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.filter(

            email=email

        ).exists():

            raise forms.ValidationError(

                "Email đã được sử dụng."

            )

        return email

    def clean(self):

        cleaned = super().clean()

        password1 = cleaned.get("password1")

        password2 = cleaned.get("password2")

        if password1 and len(password1) < 8:

            raise forms.ValidationError(
                "Mật khẩu phải có ít nhất 8 ký tự."
            )

        if password1 != password2:

            raise forms.ValidationError(
                "Mật khẩu xác nhận không khớp."
            )

        return cleaned
    
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({

                "class": "form-control"

            })