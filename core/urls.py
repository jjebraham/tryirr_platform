# core/urls.py
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("",                    views.home,                 name="home"),
    path("dashboard/",          views.dashboard,            name="dashboard"),

    # wallet
    path("wallet/",             views.wallet,               name="wallet"),
    path("wallet/deposit/",     views.wallet_deposit,       name="wallet_deposit"),
    path("wallet/withdraw/",    views.wallet_withdraw,      name="wallet_withdraw"),

    path('wallet/', views.wallet, name='wallet'),
    path('wallet/deposit/', views.wallet_deposit, name='wallet_deposit'),
    path('wallet/deposit/success/', views.wallet_deposit_success, name='wallet_deposit_success'),
    path('wallet/withdraw/', views.wallet_withdraw, name='wallet_withdraw'),
    path('wallet/withdraw/success/', views.wallet_withdraw_success, name='wallet_withdraw_success'),

    # misc / API / info
    path("rates/",              views.rates_api,            name="rates"),
    path("updates/",            views.updates,              name="updates"),
]

