import os
import random
import uuid
import requests
from django.core.mail import send_mail


GASEDAK_URL = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpSMS"


def send_phone_code(mobile: str) -> str:
    """Send a verification code via Ghasedak."""
    code = f"{random.randint(1000, 999999)}"
    payload = {
        "receptors": [{"mobile": mobile, "clientReferenceId": str(uuid.uuid4())}],
        "templateName": "Ghasedak",
        "inputs": [{"param": "Code", "value": code}],
        "udh": False,
    }
    headers = {"apikey": os.getenv("GHASEDAK_API_KEY", "")}
    try:
        r = requests.post(GASEDAK_URL, json=payload, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print("Ghasedak send error:", e)
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
