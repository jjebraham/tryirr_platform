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
    """Simple user wallet to hold balances."""

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Wallet of {self.user.username}: {self.balance}"


class Offer(models.Model):
    """P2P buy/sell offer."""

    BUY = "buy"
    SELL = "sell"
    TYPES = [
        (BUY, "Buy"),
        (SELL, "Sell"),
    ]

    IRR_TL = "IRR/TL"
    TL_IRR = "TL/IRR"
    PAIRS = [
        (IRR_TL, "IRR → TL"),
        (TL_IRR, "TL → IRR"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="offers")
    type = models.CharField(max_length=4, choices=TYPES)
    currency_pair = models.CharField(max_length=7, choices=PAIRS)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    rate = models.DecimalField(max_digits=12, decimal_places=4)
    payment_methods = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.type} {self.amount} {self.currency_pair}"


class Trade(models.Model):
    """Trade initiated from an offer between two users."""

    PENDING = "pending"
    FUNDED = "funded"
    RELEASED = "released"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (FUNDED, "Funded"),
        (RELEASED, "Released"),
    ]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="trades")
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="buy_trades")
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sell_trades")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    rate = models.DecimalField(max_digits=12, decimal_places=4)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trade #{self.pk} - {self.status}"


class ChatMessage(models.Model):
    """Chat messages exchanged within a trade."""

    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Message by {self.sender} at {self.timestamp}"


class WalletTransaction(models.Model):
    """Record of wallet deposits and withdrawals."""

    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TYPES = [
        (DEPOSIT, "Deposit"),
        (WITHDRAW, "Withdraw"),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    tx_type = models.CharField(max_length=10, choices=TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user} {self.tx_type} {self.amount}"

