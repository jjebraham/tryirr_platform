# core/views.py

from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import random
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .forms import (
    PersonalInfoForm,
    VerificationCodeForm,
    DocumentUploadForm,
    AddressProofForm,
    DepositProofForm,
    ConversionForm,
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
<<<<<<< HEAD
    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.instance.kyc_level = 1
            form.save()
            return redirect("core:dashboard")
    else:
        form = KYCForm(instance=user)
    return render(request, "core/kyc.html", {
        "form": form,
        "current_level": user.kyc_level,
    })
=======

    steps = [
        ("Personal info", user.is_personal_info_complete),
        ("Phone verification", user.is_phone_verified),
        ("Email verification", user.is_email_verified),
        ("ID & Selfie", user.is_document_uploaded),
        ("Proof of address", user.is_address_uploaded),
        ("Guarantee deposit", user.is_deposit_uploaded),
    ]

    first_incomplete = next((i + 1 for i, (_, done) in enumerate(steps) if not done), 6)
    step = int(request.GET.get("step", first_incomplete))
    if step > first_incomplete:
        return redirect(f"{reverse('core:kyc')}?step={first_incomplete}")

    if step == 1:
        form = PersonalInfoForm(request.POST or None, instance=user)
        if request.method == "POST" and form.is_valid():
            form.save()
            user.is_personal_info_complete = True
            user.save()
            send_mail("KYC step 1", "Personal info submitted", "noreply@example.com", ["admin@example.com"])
            return redirect(f"{reverse('core:kyc')}?step=2")
    elif step == 2:
        if not user.phone_verification_code:
            code = "".join(random.choices("0123456789", k=6))
            user.phone_verification_code = code
            user.save()
            send_mail("Phone code", f"Your phone verification code: {code}", "noreply@example.com", [user.email])
        form = VerificationCodeForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            if form.cleaned_data["code"] == user.phone_verification_code:
                user.is_phone_verified = True
                user.phone_verification_code = ""
                user.save()
                send_mail("KYC step 2", "Phone verified", "noreply@example.com", ["admin@example.com"])
                return redirect(f"{reverse('core:kyc')}?step=3")
            else:
                form.add_error("code", "Invalid code")
    elif step == 3:
        if not user.email_verification_code:
            code = "".join(random.choices("0123456789", k=6))
            user.email_verification_code = code
            user.save()
            send_mail("Email code", f"Your email verification code: {code}", "noreply@example.com", [user.email])
        form = VerificationCodeForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            if form.cleaned_data["code"] == user.email_verification_code:
                user.is_email_verified = True
                user.email_verification_code = ""
                user.save()
                send_mail("KYC step 3", "Email verified", "noreply@example.com", ["admin@example.com"])
                return redirect(f"{reverse('core:kyc')}?step=4")
            else:
                form.add_error("code", "Invalid code")
    elif step == 4:
        form = DocumentUploadForm(request.POST or None, request.FILES or None, instance=user)
        if request.method == "POST" and form.is_valid():
            form.save()
            user.is_document_uploaded = True
            user.save()
            send_mail("KYC step 4", "Documents uploaded", "noreply@example.com", ["admin@example.com"])
            return redirect(f"{reverse('core:kyc')}?step=5")
    elif step == 5:
        form = AddressProofForm(request.POST or None, request.FILES or None, instance=user)
        if request.method == "POST" and form.is_valid():
            form.save()
            user.is_address_uploaded = True
            user.save()
            send_mail("KYC step 5", "Address uploaded", "noreply@example.com", ["admin@example.com"])
            return redirect(f"{reverse('core:kyc')}?step=6")
    else:
        step = 6
        form = DepositProofForm(request.POST or None, request.FILES or None, instance=user)
        if request.method == "POST" and form.is_valid():
            form.save()
            user.is_deposit_uploaded = True
            user.save()
            send_mail("KYC step 6", "Deposit proof uploaded", "noreply@example.com", ["admin@example.com"])
            return redirect("core:dashboard")

    steps_context = [
        {"name": name, "done": done} for name, done in steps
    ]

    return render(
        request,
        "core/kyc.html",
        {
            "form": form,
            "step": step,
            "steps": steps_context,
            "deposit_instructions": settings.DEPOSIT_INSTRUCTIONS,
        },
    )
>>>>>>> pr-2

