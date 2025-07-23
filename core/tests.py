from django.test import TestCase
from .services.verification import send_phone_code, send_email_code


class VerificationTests(TestCase):
    def test_phone_code_returns_string(self):
        code = send_phone_code("+10000000000")
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())

    def test_email_code_returns_string(self):
        code = send_email_code("test@example.com")
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())
