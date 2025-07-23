from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Offer, ChatMessage


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

from .models import Offer, ChatMessage

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            "side",
            "currency",
            "amount",
            "price",
            "min_amount",
            "max_amount",
            "payment_methods",
        ]
        widgets = {
            "side": forms.Select(attrs={"class": "border rounded p-2"}),
            "currency": forms.Select(attrs={"class": "border rounded p-2"}),
            "amount": forms.NumberInput(attrs={"class": "border rounded p-2"}),
            "price": forms.NumberInput(attrs={"class": "border rounded p-2"}),
            "min_amount": forms.NumberInput(attrs={"class": "border rounded p-2"}),
            "max_amount": forms.NumberInput(attrs={"class": "border rounded p-2"}),
            "payment_methods": forms.TextInput(attrs={"class": "border rounded p-2 w-full"}),
        }

    def clean(self):
        cleaned = super().clean()
        amount = cleaned.get("amount")
        price = cleaned.get("price")
        min_amount = cleaned.get("min_amount")
        if amount is not None and amount <= 0:
            self.add_error("amount", "Amount must be positive")
        if price is not None and price <= 0:
            self.add_error("price", "Price must be positive")
        if amount and min_amount and min_amount > amount:
            self.add_error("min_amount", "Min amount cannot exceed total amount")
        return cleaned

class OfferFilterForm(forms.Form):
    currency = forms.ChoiceField(choices=Offer.CURRENCY_CHOICES, required=False)
    side = forms.ChoiceField(choices=Offer.SIDE_CHOICES, required=False)
    min_price = forms.DecimalField(required=False, min_value=0, decimal_places=2)
    max_price = forms.DecimalField(required=False, min_value=0, decimal_places=2)

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ["message"]
        widgets = {
            "message": forms.TextInput(attrs={"class": "border rounded p-2 w-full"})
        }
