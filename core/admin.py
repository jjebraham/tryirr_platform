from django.contrib import admin

from .models import CustomUser, SiteSettings


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "kyc_level")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "sendgrid_api_key",
        "sms_api_key",
        "telegram_api_key",
        "dark_mode_enabled",
    )
