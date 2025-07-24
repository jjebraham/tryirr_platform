from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "date_of_birth", "country"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": "border rounded p-2"}),
            "country": forms.TextInput(attrs={"class": "border rounded p-2"}),
            "first_name": forms.TextInput(attrs={"class": "border rounded p-2"}),
            "last_name": forms.TextInput(attrs={"class": "border rounded p-2"}),
        }


class VerificationCodeForm(forms.Form):
    code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={"class": "border rounded p-2"}))


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


class DocumentUploadForm(forms.ModelForm):
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
            "proof_of_address",
        ]


class GuaranteeDepositForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["deposit_proof"]


class WalletDepositForm(forms.Form):
    amount = forms.DecimalField(
        label=_("Amount"),
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "border rounded p-2 w-full", "step": "0.01"}),
    )


class WalletWithdrawForm(forms.Form):
    amount = forms.DecimalField(
        label=_("Amount"),
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "border rounded p-2 w-full", "step": "0.01"}),
    )
    address = forms.CharField(
        label=_("Destination"),
        max_length=255,
        widget=forms.TextInput(attrs={"class": "border rounded p-2 w-full"}),
    )


class ConversionForm(forms.Form):
    CHOICES = [
        ("TL_TO_IRR", _("TL → IRR")),
        ("IRR_TO_TL", _("IRR → TL")),
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


class KYCPhoneForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["phone_number"]
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "border rounded p-2"}),
        }

class KYCIdForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["id_document"]

class KYCSelfieForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["selfie"]
