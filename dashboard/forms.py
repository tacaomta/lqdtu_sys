from django import forms

class UploadCSVForm(forms.Form):
    file = forms.FileField(
    widget=forms.ClearableFileInput(

            attrs={

                "accept":
                    ".csv,.xls,.xlsx"

            }

        )
    )