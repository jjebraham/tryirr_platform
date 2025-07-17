# tryirr_platform/urls.py

from django.contrib import admin
from django.urls import path, include
from core.views import home, dashboard

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # allauth (signup / login / logout / password reset)
    path('accounts/', include('allauth.urls')),

    # Your home page
    path('', home, name='home'),

    # Post-login landing page
    path('dashboard/', dashboard, name='dashboard'),
]

