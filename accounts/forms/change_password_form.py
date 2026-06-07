from django import forms


class ChangePasswordForm(forms.Form):

    current_password = forms.CharField(

        label="Mật khẩu hiện tại",

        widget=forms.PasswordInput(

            attrs={

                "class": "form-control"

            }

        ),
        required=True,
        error_messages={"required": "Vui lòng nhập mật khẩu hiện tại"}

    )

    new_password = forms.CharField(

        label="Mật khẩu mới",

        min_length=8,

        widget=forms.PasswordInput(

            attrs={

                "class": "form-control"

            }

        ),
        required=True,
        error_messages={"required": "Vui lòng nhập mật khẩu mới"}

    )

    confirm_password = forms.CharField(

        label="Xác nhận mật khẩu mới",

        widget=forms.PasswordInput(

            attrs={

                "class": "form-control"

            }

        ),
        required=True,
        error_messages={"required": "Vui lòng xác nhận lại mật khẩu mới"}

    )

    def clean(self):

        cleaned_data = super().clean()

        new_password = cleaned_data.get(

            "new_password"

        )

        confirm_password = cleaned_data.get(

            "confirm_password"

        )
        if (new_password and len(new_password) < 8) or (confirm_password and len(confirm_password) < 8):

            raise forms.ValidationError(
                "Mật khẩu phải có ít nhất 8 ký tự."
            )

        if new_password != confirm_password:

            raise forms.ValidationError(
                "Mật khẩu xác nhận không khớp."
            )

        return cleaned_data