from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.conf import settings

from .forms import (
    PersonalInfoForm,
    VerificationCodeForm,
    PhoneVerificationForm,
    EmailVerificationForm,
    IDSelfieForm,
    ProofOfAddressForm,
    GuaranteeDepositForm,
    ConversionForm,
)
from .services.rates import fetch_try_irr_rates, fetch_all_rates
from .services.verification import send_phone_code, send_email_code


def home(request):
    return render(request, "core/index.html")


@login_required
def dashboard(request):
    rates = fetch_try_irr_rates()

    form = ConversionForm(request.GET or None)
    conversion_result = None
    if form.is_valid() and rates.TRY_IRR and rates.IRR_TRY:
        amt: Decimal = form.cleaned_data["amount"]
        rate = Decimal(str(rates.TRY_IRR)) if form.cleaned_data["direction"] == "TRY_TO_IRR" else Decimal(str(rates.IRR_TRY))
        conversion_result = amt * rate

    return render(request, "core/dashboard.html", {
        "rates": rates,
        "conversion_form": form,
        "conversion_result": conversion_result,
    })


# 🔄 KYC Wizard Implementation (PR-3)
class KYCStepMixin(LoginRequiredMixin, FormView):
    step = ""
    next_url_name = None
    prev_url_name = None

    def get_success_url(self):
        if self.next_url_name:
            return reverse(self.next_url_name)
        return reverse("core:dashboard")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["steps"] = self.get_step_statuses()
        ctx["back_url"] = reverse(self.prev_url_name) if self.prev_url_name else None      
        return ctx

    def get_step_statuses(self):
        u = self.request.user
        return [
            {"label": "Personal info", "done": True, "current": self.step == "personal"},  
            {"label": "Phone verification", "done": u.phone_verified, "current": self.step == "phone"},
            {"label": "Email verification", "done": u.email_verified, "current": self.step == "email"},
            {"label": "ID & Selfie upload", "done": bool(u.id_document and u.selfie), "current": self.step == "identity"},
            {"label": "Proof of address", "done": bool(u.address_document), "current": self.step == "address"},
            {"label": "Guarantee deposit", "done": bool(u.deposit_proof), "current": self.step == "deposit"},
        ]


class PhoneVerificationView(KYCStepMixin):
    template_name = "core/kyc_wizard/phone.html"
    form_class = PhoneVerificationForm
    step = "phone"
    next_url_name = "core:kyc_email"

    def get_initial(self):
        return {"phone_number": self.request.user.phone_number}

    def form_valid(self, form):
        action = self.request.POST.get("action")
        user = self.request.user
        if action == "send":
            user.phone_number = form.cleaned_data["phone_number"]
            user.save(update_fields=["phone_number"])
            code = send_phone_code(user.phone_number)
            self.request.session["phone_code"] = code
            self.request.session["phone_sent"] = True
            return self.render_to_response(self.get_context_data(form=form))
        elif action == "verify":
            if form.cleaned_data.get("verification_code") == self.request.session.get("phone_code"):
                user.phone_verified = True
                user.phone_number = form.cleaned_data["phone_number"]
                user.save(update_fields=["phone_number", "phone_verified"])
                self.request.session.pop("phone_code", None)
                self.request.session.pop("phone_sent", None)
                return super().form_valid(form)
            form.add_error("verification_code", "Invalid code")
        return self.form_invalid(form)


class EmailVerificationView(KYCStepMixin):
    template_name = "core/kyc_wizard/email.html"
    form_class = EmailVerificationForm
    step = "email"
    prev_url_name = "core:kyc_phone"
    next_url_name = "core:kyc_id"

    def get_initial(self):
        return {"email": self.request.user.email}

    def form_valid(self, form):
        action = self.request.POST.get("action")
        user = self.request.user
        if action == "send":
            email = form.cleaned_data["email"]
            if email != user.email:
                user.email = email
                user.save(update_fields=["email"])
            code = send_email_code(email)
            self.request.session["email_code"] = code
            self.request.session["email_sent"] = True
            return self.render_to_response(self.get_context_data(form=form))
        elif action == "verify":
            if form.cleaned_data.get("verification_code") == self.request.session.get("email_code"):
                user.email_verified = True
                user.save(update_fields=["email_verified"])
                self.request.session.pop("email_code", None)
                self.request.session.pop("email_sent", None)
                return super().form_valid(form)
            form.add_error("verification_code", "Invalid code")
        return self.form_invalid(form)


class IDSelfieView(KYCStepMixin):
    template_name = "core/kyc_wizard/id_selfie.html"
    form_class = IDSelfieForm
    step = "identity"
    prev_url_name = "core:kyc_email"
    next_url_name = "core:kyc_address"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProofOfAddressView(KYCStepMixin):
    template_name = "core/kyc_wizard/address.html"
    form_class = ProofOfAddressForm
    step = "address"
    prev_url_name = "core:kyc_id"
    next_url_name = "core:kyc_deposit"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class GuaranteeDepositView(KYCStepMixin):
    template_name = "core/kyc_wizard/deposit.html"
    form_class = GuaranteeDepositForm
    step = "deposit"
    prev_url_name = "core:kyc_address"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        if (
            user.phone_verified and user.email_verified and user.id_document and user.selfie
            and user.address_document and user.deposit_proof
        ):
            user.kyc_level = 1
            user.save()
        return redirect("core:dashboard")


@login_required
def kyc_start(request):
    u = request.user
    if not u.phone_verified:
        return redirect("core:kyc_phone")
    if not u.email_verified:
        return redirect("core:kyc_email")
    if not (u.id_document and u.selfie):
        return redirect("core:kyc_id")
    if not u.address_document:
        return redirect("core:kyc_address")
    if not u.deposit_proof:
        return redirect("core:kyc_deposit")
    return redirect("core:dashboard")


@login_required
def verification(request):
    """Alias for the KYC view so /verification/ stays functional."""
    return kyc_start(request)


def rates_api(request):
    """Return exchange rates as JSON for the homepage table."""
    data = fetch_all_rates()
    if not data:
        return JsonResponse({"error": "unavailable"}, status=503)
    return JsonResponse(data)

