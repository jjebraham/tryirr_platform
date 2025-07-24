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
        blank=True
    )
    deposit_proof = models.FileField(
        upload_to="kyc/deposit/",
        null=True,
        blank=True
    )

    # Address proof
    address_country = models.CharField(max_length=100, null=True, blank=True)
    address_city = models.CharField(max_length=100, null=True, blank=True)
    address_zip = models.CharField(max_length=20, null=True, blank=True)
    address_street = models.CharField(max_length=255, null=True, blank=True)
    address_document = models.FileField(
        upload_to="kyc/address/",
        null=True,
        blank=True,
    )

    # Guarantee deposit
    deposit_proof = models.FileField(
        upload_to="kyc/deposit/",
        null=True,
        blank=True,
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


class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance_try = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    balance_irr = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"Wallet of {self.user}" 

class Offer(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    SIDE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]
    TRY = 'TRY'
    IRR = 'IRR'
    CURRENCY_CHOICES = [
        (TRY, 'TRY'),
        (IRR, 'IRR'),
    ]

    side = models.CharField(max_length=4, choices=SIDE_CHOICES)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=TRY)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_methods = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.side} {self.amount} {self.currency} @ {self.price}" 

class Trade(models.Model):
    OPEN = 'OPEN'
    PAID = 'PAID'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (PAID, 'Paid'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    buyer = models.ForeignKey(CustomUser, related_name='buy_trades', on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, related_name='sell_trades', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trade #{self.pk} {self.status}" 

class ChatMessage(models.Model):
    trade = models.ForeignKey(Trade, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Msg by {self.user} on trade {self.trade_id}" 
