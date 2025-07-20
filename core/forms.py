# core/forms.py

from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class KYCForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "phone_number",
            "id_document",
            "selfie",
        ]
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "border rounded p-2"}),
            # file‑inputs get their own default widget
        }

class ConversionForm(forms.Form):
    CHOICES = [
        ("TRY_TO_IRR", _("TRY → IRR")),
        ("IRR_TO_TRY", _("IRR → TRY")),
    ]
    direction = forms.ChoiceField(
        label=_("Convert"),
        choices=CHOICES,
        widget=forms.Select(attrs={"class": "border rounded p-2"})
    )
    amount = forms.DecimalField(
        label=_("Amount"),
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"class": "border rounded p-2", "step": "0.01"}
        )
    )

