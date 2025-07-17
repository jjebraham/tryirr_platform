from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # allauth (signup / login / logout / pw reset)
    path('accounts/', include('allauth.urls')),

    # your core app
    path('', include('core.urls', namespace='core')),
]

