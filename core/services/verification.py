import os
import random
import requests
from django.core.mail import send_mail
from django.conf import settings

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")


def send_phone_code(phone: str) -> str:
    """Send a verification code via SMS using Twilio if configured."""
    code = f"{random.randint(100000, 999999)}"
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
        data = {
            "To": phone,
            "From": TWILIO_FROM_NUMBER,
            "Body": f"Your verification code is {code}",
        }
        try:
            requests.post(
                url,
                data=data,
                auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
                timeout=10,
            )
        except Exception as exc:
            print("Failed to send SMS:", exc)
    else:
        print(f"Sending SMS to {phone}: {code}")
    return code


def send_email_code(email: str) -> str:
    """Send a verification code via email."""
    code = f"{random.randint(100000, 999999)}"
    send_mail(
        "Your verification code",
        f"Your verification code is {code}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=True,
    )
    return code
