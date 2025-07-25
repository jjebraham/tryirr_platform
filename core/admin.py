from django.contrib import admin

from .models import IntegrationSettings


@admin.register(IntegrationSettings)
class IntegrationSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow adding if no settings exist
        if IntegrationSettings.objects.exists():
            return False
        return super().has_add_permission(request)
