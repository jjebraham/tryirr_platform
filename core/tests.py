import os
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import CustomUser
from .services import verification


class SendGridEmailTests(TestCase):
    @patch("core.services.verification.urllib.request.urlopen")
    def test_send_email_code_uses_sendgrid(self, mock_urlopen):
        with patch.dict(os.environ, {"SENDGRID_API_KEY": "SG.TEST"}):
            code = verification.send_email_code("user@example.com")
        self.assertEqual(len(code), 6)
        self.assertTrue(mock_urlopen.called)


class SendCodeViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="u", password="p")

    @patch("core.services.verification.send_phone_code")
    def test_send_code_endpoint(self, mock_send):
        mock_send.return_value = "123456"
        self.client.login(username="u", password="p")
        resp = self.client.post(reverse("core:send_code"), {"kind": "phone", "target": "123"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get("success"), True)
