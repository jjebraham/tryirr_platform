import random
from django.core.mail import send_mail

try:
    import requests
except Exception:  # pragma: no cover - optional dependency
    requests = None

from ..models import SiteConfiguration


def send_phone_code(phone: str) -> str:
    """Send an SMS verification code via Ghasedak."""
    code = f"{random.randint(100000, 999999)}"
    settings = SiteConfiguration.objects.first()
    api_key = settings.ghasedak_api_key if settings else ""
    template = settings.ghasedak_template_name if settings else ""

    if requests:
        url = "https://api.ghasedak.io/v2/verification/send/simple"
        headers = {"apikey": api_key}
        data = {"receptor": phone, "template": template, "type": 1, "param1": code}
        try:
            requests.post(url, data=data, headers=headers, timeout=10)
        except Exception as exc:  # pragma: no cover - network
            print(f"Ghasedak request failed: {exc}")
    else:  # pragma: no cover - fallback
        print(f"Sending SMS to {phone}: {code}")
    return code


def send_email_code(email: str) -> str:
    """Send a verification code via Mailgrid."""
    code = f"{random.randint(100000, 999999)}"
    settings = SiteConfiguration.objects.first()
    api_key = settings.mailgrid_api_key if settings else ""
    sender = settings.mailgrid_sender if settings else None

    if requests:
        url = "https://api.mailgrid.ir/v1/send"
        headers = {"Authorization": f"Bearer {api_key}"}
        json = {
            "from": sender,
            "to": [email],
            "subject": "Your verification code",
            "text": f"Your verification code is {code}",
        }
        try:
            requests.post(url, json=json, headers=headers, timeout=10)
        except Exception as exc:  # pragma: no cover - network
            print(f"Mailgrid request failed: {exc}")
    else:
        send_mail(
            "Your verification code",
            f"Your verification code is {code}",
            sender,
            [email],
            fail_silently=True,
        )
    return code
