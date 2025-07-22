# core/views.py

from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path
from .forms import (
    KYCForm,
    ConversionForm,
    KYCPhoneForm,
    KYCIdForm,
    KYCSelfieForm,
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
    return render(request, "core/kyc.html", {
        "form": form,
        "current_level": user.kyc_level,
    })


@login_required
def kyc_wizard(request):
    step = int(request.GET.get("step", 1))
    user = request.user

    if step <= 1:
        FormClass = KYCPhoneForm
        next_step = 2
    elif step == 2:
        FormClass = KYCIdForm
        next_step = 3
    else:
        FormClass = KYCSelfieForm
        next_step = None

    form = FormClass(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        form.save()
        if next_step:
            return redirect(f"{request.path}?step={next_step}")
        else:
            user.kyc_level = 1
            user.save()
            return redirect("core:dashboard")

    return render(request, "core/kyc_wizard.html", {"form": form, "step": step})


def live_rates(request):
    rates = fetch_try_irr_rates()
    return JsonResponse({"TRY_IRR": rates.TRY_IRR, "IRR_TRY": rates.IRR_TRY})


def updates(request):
    updates_file = Path(settings.BASE_DIR) / "UPDATES.md"
    try:
        content = updates_file.read_text()
    except Exception:
        content = "No updates available."
    return render(request, "core/updates.html", {"content": content})
