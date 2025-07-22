# core/views.py

from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    PhoneVerificationForm,
    EmailVerificationForm,
    IDSelfieForm,
    ProofOfAddressForm,
    GuaranteeDepositForm,
>>>>>>> pr-3
    ConversionForm,
)
from .services.rates import fetch_try_irr_rates
from .services.verification import send_phone_code, send_email_code
=======
from .forms import KYCForm, ConversionForm
from .services.rates import fetch_try_irr_rates, fetch_all_rates
from django.http import JsonResponse
>>>>>>> pr-5

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

<<<<<<< HEAD
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
=======

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
            user.phone_verified
            and user.email_verified
            and user.id_document
            and user.selfie
            and user.address_document
            and user.deposit_proof
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
>>>>>>> pr-3


@login_required
def verification(request):
    """Alias for the KYC view so /verification/ stays functional."""
    return kyc(request)


def rates_api(request):
    """Return exchange rates as JSON for the homepage table."""
    data = fetch_all_rates()
    if not data:
        return JsonResponse({"error": "unavailable"}, status=503)
    return JsonResponse(data)

