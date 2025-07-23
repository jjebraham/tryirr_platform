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
            "address_document",
        ]


class GuaranteeDepositForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["deposit_proof"]


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


class OfferForm(forms.ModelForm):
    class Meta:
        from .models import Offer
        model = Offer
        fields = ["type", "currency_pair", "amount", "rate", "payment_methods"]
        widgets = {
            "type": forms.Select(attrs={"class": "border rounded p-2"}),
            "currency_pair": forms.Select(attrs={"class": "border rounded p-2"}),
            "amount": forms.NumberInput(attrs={"class": "border rounded p-2"}),
            "rate": forms.NumberInput(attrs={"class": "border rounded p-2"}),
            "payment_methods": forms.TextInput(attrs={"class": "border rounded p-2 w-full"}),
        }


class ChatMessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "border rounded p-2 w-full", "rows": 3}))


class DepositForm(forms.Form):
    amount = forms.DecimalField(min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={"class": "border rounded p-2"}))


class WithdrawForm(forms.Form):
    amount = forms.DecimalField(min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={"class": "border rounded p-2"}))
