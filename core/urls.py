from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),

    # Post‑login dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

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

    # Marketplace
    path('offers/', views.OfferListView.as_view(), name='offer_list'),
    path('offers/new/', views.OfferCreateView.as_view(), name='offer_create'),
    path('offers/<int:pk>/', views.OfferDetailView.as_view(), name='offer_detail'),

    path('trades/<int:pk>/', views.TradeDetailView.as_view(), name='trade_detail'),
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    path('transactions/', views.TransactionListView.as_view(), name='transactions'),
]

