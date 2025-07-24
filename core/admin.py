from django.contrib import admin

from .models import CustomUser, SiteSettings


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "phone_number", "kyc_level"]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fields = ["sendgrid_api_key", "sms_api_key", "telegram_bot_token"]
