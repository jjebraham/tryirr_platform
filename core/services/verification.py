import random
from django.core.mail import send_mail


def send_phone_code(phone: str) -> str:
    """Simulate sending an SMS verification code."""
    code = f"{random.randint(100000, 999999)}"
    print(f"Sending SMS to {phone}: {code}")
    return code


def send_email_code(email: str) -> str:
    """Send a verification code via email."""
    code = f"{random.randint(100000, 999999)}"
    send_mail(
        "Your verification code",
        f"Your verification code is {code}",
        None,
        [email],
        fail_silently=True,
    )
    return code
