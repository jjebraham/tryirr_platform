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
    path('kyc/',         views.kyc,         name='kyc'),
    path('kyc/wizard/', views.kyc_wizard, name='kyc_wizard'),

    # API
    path('api/live_rates/', views.live_rates, name='live_rates'),

    # Updates page
    path('updates/', views.updates, name='updates'),
]

