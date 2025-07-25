import os
import json
import random
import urllib.request

from django.conf import settings


def send_phone_code(phone: str) -> str:
    """Send a verification code via Ghasedak API."""
    code = f"{random.randint(100000, 999999)}"
    api_key = os.getenv("GHASEDAK_API_KEY")
    if api_key:
        data = urllib.parse.urlencode({
            "receptor": phone,
            "message": f"Your verification code is {code}",
        }).encode()
        req = urllib.request.Request(
            "https://api.ghasedak.me/v2/sms/send/simple", data=data
        )
        req.add_header("apikey", api_key)
        try:
            with urllib.request.urlopen(req) as resp:
                resp.read()
        except Exception as e:
            print("Ghasedak error", e)
    else:
        print("Ghasedak API key missing; SMS not sent")
    return code


def send_email_code(email: str) -> str:
    """Send a verification code via SendGrid."""
    code = f"{random.randint(100000, 999999)}"
    api_key = os.getenv("SENDGRID_API_KEY") or getattr(settings, "SENDGRID_API_KEY", "")
    if api_key:
        payload = json.dumps({
            "personalizations": [{"to": [{"email": email}]}],
            "from": {"email": "no-reply@example.com"},
            "subject": "Your verification code",
            "content": [{"type": "text/plain", "value": f"Your verification code is {code}"}],
        }).encode()
        req = urllib.request.Request(
            "https://api.sendgrid.com/v3/mail/send",
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req) as resp:
                resp.read()
        except Exception as e:
            print("SendGrid error", e)
    else:
        print("SendGrid API key missing; email not sent")
    return code
