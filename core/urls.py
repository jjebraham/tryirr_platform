# core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Landing page
    path('',     views.home,      name='home'),
    # Post‑login dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # KYC flow
    path('kyc/',  views.kyc,       name='kyc'),
    path('verification/', views.verification, name='verification'),
    path('rates/', views.rates_api, name='rates'),
]

