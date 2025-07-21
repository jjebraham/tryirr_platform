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


class PhoneVerificationForm(forms.Form):
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "border rounded p-2 w-full"}))
    verification_code = forms.CharField(max_length=6, required=False, widget=forms.TextInput(attrs={"class": "border rounded p-2 w-full"}))


class EmailVerificationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "border rounded p-2 w-full"}))
    verification_code = forms.CharField(max_length=6, required=False, widget=forms.TextInput(attrs={"class": "border rounded p-2 w-full"}))


class IDSelfieForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["id_document", "selfie"]


class ProofOfAddressForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "address_country",
            "address_city",
            "address_zip",
            "address_street",
            "address_document",
        ]


class GuaranteeDepositForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["deposit_proof"]

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

