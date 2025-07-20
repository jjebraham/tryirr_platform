from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, VerificationSettings


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Verification", {
            "fields": (
                "kyc_level",
                "email_verified",
                "phone_verified",
                "two_factor_enabled",
                "address_verified",
                "deposit_verified",
            )
        }),
    )


@admin.register(VerificationSettings)
class VerificationSettingsAdmin(admin.ModelAdmin):
    list_display = [
        "phone_api_key",
        "phone_endpoint",
        "email_api_key",
        "email_smtp_server",
    ]
