# core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Landing page
    path('',     views.home,      name='home'),
    # Post‑login dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # Verification center
    path('verification/', views.VerificationIndexView.as_view(), name='verification'),
    # Updates log (admins only)
    path('updates/', views.UpdatesView.as_view(), name='updates'),
    # KYC flow
    path('kyc/',  views.kyc,       name='kyc'),
]

