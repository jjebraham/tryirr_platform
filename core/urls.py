# core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Landing page
    path('',     views.home,      name='home'),
    # Post‑login dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # KYC wizard
    path('kyc/', views.kyc_start, name='kyc'),
    path('kyc/phone/',   views.PhoneVerificationView.as_view(),    name='kyc_phone'),
    path('kyc/email/',   views.EmailVerificationView.as_view(),    name='kyc_email'),
    path('kyc/id/',      views.IDSelfieView.as_view(),             name='kyc_id'),
    path('kyc/address/', views.ProofOfAddressView.as_view(),       name='kyc_address'),
    path('kyc/deposit/', views.GuaranteeDepositView.as_view(),     name='kyc_deposit'),
]

