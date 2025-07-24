# core/urls.py
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # Public pages
    path("", views.home, name="home"),
    path("rates/", views.rates_api, name="rates"),
    path("updates/", views.updates, name="updates"),

    # Authenticated pages
    path("dashboard/", views.dashboard, name="dashboard"),
    path("verification/", views.verification, name="verification"),  # Verification Center

    # KYC wizard
    path("kyc/", views.kyc_start, name="kyc_start"),
    path("kyc/phone/", views.PhoneVerificationView.as_view(), name="kyc_phone"),
    path("kyc/email/", views.EmailVerificationView.as_view(), name="kyc_email"),
    path("kyc/id/", views.IDSelfieView.as_view(), name="kyc_id"),
    path("kyc/address/", views.ProofOfAddressView.as_view(), name="kyc_address"),
    path("kyc/deposit/", views.GuaranteeDepositView.as_view(), name="kyc_deposit"),

    # Wallet flows
    path("wallet/", views.wallet, name="wallet"),
    path("wallet/deposit/", views.wallet_deposit, name="wallet_deposit"),
    path("wallet/deposit/success/", views.wallet_deposit_success, name="wallet_deposit_success"),
    path("wallet/withdraw/", views.wallet_withdraw, name="wallet_withdraw"),
    path("wallet/withdraw/success/", views.wallet_withdraw_success, name="wallet_withdraw_success"),
]

