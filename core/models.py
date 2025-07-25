# core/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    kyc_level = models.PositiveIntegerField(default=0)  # Level 0 = unverified

    # Personal info
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    # Step tracking
    is_personal_info_complete = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_document_uploaded = models.BooleanField(default=False)
    is_address_uploaded = models.BooleanField(default=False)
    is_deposit_uploaded = models.BooleanField(default=False)

    phone_verification_code = models.CharField(max_length=6, null=True, blank=True)
    email_verification_code = models.CharField(max_length=6, null=True, blank=True)

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
    proof_of_address = models.FileField(
        upload_to="kyc/address/",
        null=True,
        blank=True,
    )
    deposit_proof = models.FileField(
        upload_to="kyc/deposit/",
        null=True,
        blank=True,
    )

    # Address proof
    address_country = models.CharField(max_length=100, null=True, blank=True)
    address_city = models.CharField(max_length=100, null=True, blank=True)
    address_zip = models.CharField(max_length=20, null=True, blank=True)
    address_street = models.CharField(max_length=255, null=True, blank=True)

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


class IntegrationSettings(models.Model):
    ghasedak_api_key = models.CharField(max_length=255)
    ghasedak_template_name = models.CharField(max_length=100)
    mailgrid_api_key = models.CharField(max_length=255)
    mailgrid_sender_email = models.EmailField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        IntegrationSettings.objects.exclude(id=self.id).delete()

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls()
            obj.save()
        return obj

    def __str__(self):
        return "Integration Settings"



class SiteConfiguration(models.Model):
    ghasedak_api_key = models.CharField(max_length=255, blank=True)
    ghasedak_template_name = models.CharField(max_length=255, blank=True)
    mailgrid_api_key = models.CharField(max_length=255, blank=True)
    mailgrid_sender = models.EmailField(blank=True)

    class Meta:
        verbose_name = "Site configuration"
        verbose_name_plural = "Site configuration"

    def __str__(self):
        return "Site configuration"
