from django import forms

from users.models import UserProfile


class ProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = [

            "fullname",

            "department"

        ]

        widgets = {

            "fullname": forms.TextInput(

                attrs={

                    "class": "form-control"

                }

            ),

            "department": forms.Select(

                attrs={

                    "class": "form-select"

                }

            )

        }