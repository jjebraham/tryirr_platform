# core/views.py

from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import KYCForm, ConversionForm
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

