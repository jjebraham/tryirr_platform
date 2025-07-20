# core/views.py

from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django import forms
from django.utils.decorators import method_decorator
from .forms import (
    KYCForm,
    ConversionForm,
    EmailVerificationForm,
    PhoneVerificationForm,
    TwoFactorForm,
    IDSelfieForm,
    ProofOfAddressForm,
    DepositProofForm,
)
from .services.rates import fetch_try_irr_rates

def home(request):
    return render(request, "core/index.html")

@login_required
def dashboard(request):
    # fetch fresh TRY↔IRR rates
    rates = fetch_try_irr_rates()

    # wire up the converter form
    form = ConversionForm(request.GET or None)
    conversion_result = None
    if form.is_valid() and rates.TRY_IRR and rates.IRR_TRY:
        amt: Decimal = form.cleaned_data["amount"]
        if form.cleaned_data["direction"] == "TRY_TO_IRR":
            # convert the float rate into Decimal
            rate = Decimal(str(rates.TRY_IRR))
        else:
            rate = Decimal(str(rates.IRR_TRY))
        conversion_result = amt * rate

    return render(request, "core/dashboard.html", {
        "rates": rates,
        "conversion_form": form,
        "conversion_result": conversion_result,
    })

@login_required
def kyc(request):
    user = request.user
    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.instance.kyc_level = 1
            form.save()
            return redirect("core:dashboard")
    else:
        form = KYCForm(instance=user)
    return render(request, "core/kyc.html", {"form": form})


class VerificationCenterView(View):
    """Multi-step verification wizard."""

    steps = [
        {"label": "Personal Info", "form": None},
        {"label": "Email Verification", "form": EmailVerificationForm},
        {"label": "Phone Verification", "form": PhoneVerificationForm},
        {"label": "Two-Factor Auth", "form": TwoFactorForm},
        {"label": "ID & Selfie", "form": IDSelfieForm},
        {"label": "Proof of Address", "form": ProofOfAddressForm},
        {"label": "Deposit Proof", "form": DepositProofForm},
    ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        step = int(request.GET.get("step", 1))
        step = max(1, min(step, len(self.steps)))
        form_class = self.steps[step - 1]["form"]
        form = form_class(instance=request.user) if form_class and issubclass(form_class, forms.ModelForm) else (form_class() if form_class else None)
        context = {
            "step": step,
            "form": form,
            "steps": self.steps,
        }
        return render(request, f"core/verification/step_{step}.html", context)

    def post(self, request):
        step = int(request.POST.get("step", 1))
        form_class = self.steps[step - 1]["form"]
        if form_class is None:
            return redirect(f"{request.path}?step={step+1}")
        if issubclass(form_class, forms.ModelForm):
            form = form_class(request.POST, request.FILES, instance=request.user)
        else:
            form = form_class(request.POST)
        if form.is_valid():
            user = request.user
            if step == 2:
                user.email_verified = True
                user.kyc_level = max(user.kyc_level, 1)
            elif step == 3:
                user.phone_verified = True
                user.kyc_level = max(user.kyc_level, 2)
            elif step == 4:
                user.two_factor_enabled = True
                user.kyc_level = max(user.kyc_level, 3)
            elif step == 5:
                user.id_document = form.cleaned_data.get("id_document")
                user.selfie = form.cleaned_data.get("selfie")
                user.kyc_level = max(user.kyc_level, 4)
            elif step == 6:
                user.address_country = form.cleaned_data.get("address_country")
                user.address_city = form.cleaned_data.get("address_city")
                user.address_zip = form.cleaned_data.get("address_zip")
                user.address_street = form.cleaned_data.get("address_street")
                user.proof_of_address = form.cleaned_data.get("proof_of_address")
                user.address_verified = True
                user.kyc_level = max(user.kyc_level, 5)
            elif step == 7:
                user.deposit_receipt = form.cleaned_data.get("deposit_receipt")
                user.deposit_verified = True
                user.kyc_level = max(user.kyc_level, 6)
            user.save()
            return redirect(f"{request.path}?step={step+1}")
        context = {
            "step": step,
            "form": form,
            "steps": self.steps,
        }
        return render(request, f"core/verification/step_{step}.html", context)

