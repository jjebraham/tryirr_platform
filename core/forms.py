from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
import re


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


import re


class PhoneNumberWidget(forms.TextInput):
    """Input with a fixed +98 prefix."""
    template_name = "widgets/phone_input.html"

    def __init__(self, attrs=None):
        attrs = attrs or {}
        default = attrs.get("class", "")
        attrs["class"] = (default + " border rounded p-2 w-full").strip()
        attrs.setdefault("maxlength", "10")
        super().__init__(attrs)


class PhoneVerificationForm(forms.Form):
    phone_number = forms.CharField(
        label="Phone number",
        max_length=10,
        help_text="Enter the 10 digit number",
        widget=PhoneNumberWidget(),
    )
    verification_code = forms.CharField(
        label="Verification code",
        max_length=6,
        required=False,
        widget=forms.TextInput(attrs={"class": "border rounded p-2 w-full"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = self.initial.get("phone_number")
        if initial and initial.startswith("+98"):
            self.initial["phone_number"] = initial[3:]

    def clean_phone_number(self):
        number = self.cleaned_data["phone_number"].strip()
        if number.startswith("+98"):
            number = number[3:]
        if not re.fullmatch(r"\d{10}", number):
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return f"+98{number}"


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
