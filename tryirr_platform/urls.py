# tryirr_platform/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # allauth
    path('accounts/', include('allauth.urls')),

    # all of your "core" app’s URLs, under the "core" namespace
    path('', include(('core.urls', 'core'), namespace='core')),
]

