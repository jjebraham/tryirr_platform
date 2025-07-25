# tryirr_platform/core/urls.py

from django.urls import path
from . import views
from .views import (
    PhoneVerificationView,
    EmailVerificationView,
    IDSelfieView,
    ProofOfAddressView,
    GuaranteeDepositView,
)

app_name = "core"

urlpatterns = [
    # Landing page
    path("", views.home, name="home"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Wallet
    path("wallet/", views.wallet, name="wallet"),
    path("wallet/deposit/", views.wallet_deposit, name="wallet_deposit"),
    path("wallet/deposit/success/", views.wallet_deposit_success, name="wallet_deposit_success"),
    path("wallet/withdraw/", views.wallet_withdraw, name="wallet_withdraw"),
    path("wallet/withdraw/success/", views.wallet_withdraw_success, name="wallet_withdraw_success"),

    # KYC wizard entry and steps
    path("kyc/", views.kyc_start, name="kyc"),
    path("kyc/phone/",    PhoneVerificationView.as_view(),   name="kyc_phone"),
    path("kyc/email/",    EmailVerificationView.as_view(),   name="kyc_email"),
    path("kyc/id/",       IDSelfieView.as_view(),            name="kyc_id"),
    path("kyc/address/",  ProofOfAddressView.as_view(),      name="kyc_address"),
    path("kyc/deposit/",  GuaranteeDepositView.as_view(),    name="kyc_deposit"),

    # Verification center
    path("verification/", views.verification, name="verification"),

    # Rates endpoints — give the JSON‐feed URL the name "rates" since your template uses that
    path("api/rates/",     views.rates_api,   name="rates"),
    path("api/live_rates/",views.live_rates,  name="live_rates"),

    # Updates page
    path("updates/", views.updates, name="updates"),
]

