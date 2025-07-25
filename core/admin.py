from django.contrib import admin

from .models import IntegrationSettings, SiteConfiguration


@admin.register(IntegrationSettings)
class IntegrationSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ("ghasedak_api_key", "mailgrid_sender",)
