from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),

    # Post‑login dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    path('wallet/', views.wallet, name='wallet'),
    path('wallet/deposit/', views.wallet_deposit, name='wallet_deposit'),
    path('wallet/deposit/success/', views.wallet_deposit_success, name='wallet_deposit_success'),
    path('wallet/withdraw/', views.wallet_withdraw, name='wallet_withdraw'),
    path('wallet/withdraw/success/', views.wallet_withdraw_success, name='wallet_withdraw_success'),

    # ✅ KYC Wizard Views
    path('kyc/', views.kyc_start, name='kyc'),
    path('kyc/phone/',   views.PhoneVerificationView.as_view(),    name='kyc_phone'),      
    path('kyc/email/',   views.EmailVerificationView.as_view(),    name='kyc_email'),      
    path('kyc/id/',      views.IDSelfieView.as_view(),             name='kyc_id'),
    path('kyc/address/', views.ProofOfAddressView.as_view(),       name='kyc_address'),    
    path('kyc/deposit/', views.GuaranteeDepositView.as_view(),     name='kyc_deposit'),    

    # ✅ Extra Views
    path('verification/', views.verification, name='verification'),
    path('rates/', views.rates_api, name='rates'),
    path('updates/', views.updates, name='updates'),
    path('live-rates/', views.live_rates, name='live_rates'),
]

