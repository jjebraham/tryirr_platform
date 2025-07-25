from django.contrib import admin

from .models import IntegrationSettings


@admin.register(IntegrationSettings)
class IntegrationSettingsAdmin(admin.ModelAdmin):
    pass
