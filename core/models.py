# core/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    kyc_level = models.PositiveIntegerField(default=0)  # Level 0 = unverified

    # KYC uploads
    id_document = models.FileField(
        upload_to="kyc/id_documents/",
        null=True,
        blank=True,
        help_text="A scan or photo of your government‑issued ID."
    )
    selfie = models.FileField(
        upload_to="kyc/selfies/",
        null=True,
        blank=True,
        help_text="A selfie of you holding your ID next to your face."
    )

    # Verification flags and extra data
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    address_verified = models.BooleanField(default=False)
    deposit_verified = models.BooleanField(default=False)

    proof_of_address = models.FileField(
        upload_to="kyc/address_proofs/",
        null=True,
        blank=True,
    )
    deposit_receipt = models.FileField(
        upload_to="kyc/deposit_receipts/",
        null=True,
        blank=True,
    )

    address_country = models.CharField(max_length=100, blank=True)
    address_city = models.CharField(max_length=100, blank=True)
    address_zip = models.CharField(max_length=20, blank=True)
    address_street = models.CharField(max_length=255, blank=True)

    # Override groups/permissions to avoid clashes:
    groups = models.ManyToManyField(
        Group, blank=True, related_name="customuser_set",
        help_text="The groups this user belongs to."
    )
    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name="customuser_set",
        help_text="Specific permissions for this user."
    )

    def __str__(self):
        return f"{self.username} ({self.phone_number})"


class VerificationSettings(models.Model):
    """Site-wide settings for verification services."""

    phone_api_key = models.CharField(max_length=255, blank=True)
    phone_endpoint = models.CharField(max_length=255, blank=True)

    email_api_key = models.CharField(max_length=255, blank=True)
    email_smtp_server = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Verification Settings"

    def __str__(self):
        return "Verification Settings"

