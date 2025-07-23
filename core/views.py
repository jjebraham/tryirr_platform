from decimal import Decimal
from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.conf import settings
from django.db import models

from .forms import (
    PersonalInfoForm,
    VerificationCodeForm,
    PhoneVerificationForm,
    EmailVerificationForm,
    IDSelfieForm,
    ProofOfAddressForm,
    GuaranteeDepositForm,
    ConversionForm,
    OfferForm,
    ChatMessageForm,
    DepositForm,
    WithdrawForm,
)
from .models import Offer, Trade, ChatMessage, Wallet, WalletTransaction
from .services.rates import fetch_try_irr_rates, fetch_all_rates
from .services.verification import send_phone_code, send_email_code


def home(request):
    return render(request, "core/index.html")


@login_required
def dashboard(request):
    rates = fetch_try_irr_rates()

    form = ConversionForm(request.GET or None)
    conversion_result = None
    if form.is_valid() and rates.TL_IRR and rates.IRR_TL:
        amt: Decimal = form.cleaned_data["amount"]
        rate = Decimal(str(rates.TL_IRR)) if form.cleaned_data["direction"] == "TL_TO_IRR" else Decimal(str(rates.IRR_TL))
        conversion_result = amt * rate

    return render(request, "core/dashboard.html", {
        "rates": rates,
        "conversion_form": form,
        "conversion_result": conversion_result,
    })


# 🔄 KYC Wizard Implementation
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
    return kyc_start(request)


def rates_api(request):
    data = fetch_all_rates()
    if not data:
        return JsonResponse({"error": "unavailable"}, status=503)
    return JsonResponse(data)


def live_rates(request):
    rates = fetch_try_irr_rates()
    return JsonResponse({
        "TL_IRR": rates.TL_IRR,
        "IRR_TL": rates.IRR_TL,
        "USDT_TL": rates.USDT_TL,
        "TL_USDT": rates.TL_USDT,
    })


def updates(request):
    updates_file = Path(settings.BASE_DIR) / "UPDATES.md"
    try:
        content = updates_file.read_text()
    except Exception:
        content = "No updates available."
    return render(request, "core/updates.html", {"content": content})


# ─── Marketplace Views ────────────────────────────────────────────────────────


class OfferListView(ListView):
    model = Offer
    template_name = "core/offers/list.html"
    context_object_name = "offers"

    def get_queryset(self):
        qs = Offer.objects.filter(active=True)
        pair = self.request.GET.get("pair")
        min_amt = self.request.GET.get("min")
        max_amt = self.request.GET.get("max")
        if pair:
            qs = qs.filter(currency_pair=pair)
        if min_amt:
            qs = qs.filter(amount__gte=min_amt)
        if max_amt:
            qs = qs.filter(amount__lte=max_amt)
        return qs.order_by("-created_at")


class OfferCreateView(LoginRequiredMixin, CreateView):
    model = Offer
    form_class = OfferForm
    template_name = "core/offers/form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("core:offer_detail", args=[self.object.pk])


class OfferDetailView(LoginRequiredMixin, DetailView):
    model = Offer
    template_name = "core/offers/detail.html"
    context_object_name = "offer"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        trade = Trade.objects.create(
            offer=self.object,
            buyer=request.user if self.object.type == Offer.SELL else self.object.user,
            seller=self.object.user if self.object.type == Offer.SELL else request.user,
            amount=self.object.amount,
            rate=self.object.rate,
        )
        return redirect("core:trade_detail", trade.pk)


class TradeDetailView(LoginRequiredMixin, DetailView, FormView):
    model = Trade
    template_name = "core/trades/detail.html"
    form_class = ChatMessageForm
    context_object_name = "trade"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop("instance", None)
        return kwargs

    def get_queryset(self):
        user = self.request.user
        return Trade.objects.filter(buyer=user) | Trade.objects.filter(seller=user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["messages"] = self.object.messages.all()
        ctx["can_fund"] = self.object.status == Trade.PENDING and self.request.user == self.object.buyer
        ctx["can_release"] = self.object.status == Trade.FUNDED and self.request.user == self.object.seller
        return ctx

    def form_valid(self, form):
        trade = self.get_object()
        if self.request.user not in [trade.buyer, trade.seller]:
            return redirect("core:dashboard")
        ChatMessage.objects.create(
            trade=trade,
            sender=self.request.user,
            message=form.cleaned_data["message"],
        )
        return redirect("core:trade_detail", trade.pk)

    def post(self, request, *args, **kwargs):
        if "fund" in request.POST:
            trade = self.get_object()
            if trade.status == Trade.PENDING and request.user == trade.buyer:
                trade.status = Trade.FUNDED
                trade.save(update_fields=["status"])
            return redirect("core:trade_detail", trade.pk)
        if "release" in request.POST:
            trade = self.get_object()
            if trade.status == Trade.FUNDED and request.user == trade.seller:
                trade.status = Trade.RELEASED
                trade.save(update_fields=["status"])
            return redirect("core:trade_detail", trade.pk)
        return super().post(request, *args, **kwargs)


class WalletView(LoginRequiredMixin, FormView):
    template_name = "core/wallet.html"
    form_class = DepositForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        ctx["wallet"] = wallet
        ctx["withdraw_form"] = WithdrawForm()
        return ctx

    def form_valid(self, form):
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        if "deposit" in self.request.POST:
            wallet.balance += form.cleaned_data["amount"]
            wallet.save(update_fields=["balance"])
            WalletTransaction.objects.create(wallet=wallet, tx_type=WalletTransaction.DEPOSIT, amount=form.cleaned_data["amount"])
        elif "withdraw" in self.request.POST:
            withdraw_form = WithdrawForm(self.request.POST)
            if withdraw_form.is_valid() and wallet.balance >= withdraw_form.cleaned_data["amount"]:
                wallet.balance -= withdraw_form.cleaned_data["amount"]
                wallet.save(update_fields=["balance"])
                WalletTransaction.objects.create(wallet=wallet, tx_type=WalletTransaction.WITHDRAW, amount=withdraw_form.cleaned_data["amount"])
        return redirect("core:wallet")


class TransactionListView(LoginRequiredMixin, ListView):
    template_name = "core/transactions.html"
    context_object_name = "transactions"

    def get_queryset(self):
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        txs = list(wallet.transactions.all())
        trades = list(Trade.objects.filter(status=Trade.RELEASED).filter(models.Q(buyer=self.request.user) | models.Q(seller=self.request.user)))
        return sorted(txs + trades, key=lambda x: x.created_at if isinstance(x, Trade) else x.timestamp, reverse=True)

