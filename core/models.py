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

