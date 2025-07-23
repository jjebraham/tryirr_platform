from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Offer, Trade, Wallet


class OfferTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="u", password="p")

    def test_create_offer(self):
        self.client.login(username="u", password="p")
        resp = self.client.post(reverse("core:offer_create"), {
            "type": Offer.BUY,
            "currency_pair": Offer.IRR_TL,
            "amount": "100",
            "rate": "1",
            "payment_methods": "bank",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Offer.objects.count(), 1)


class WalletTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="w", password="p")

    def test_deposit(self):
        self.client.login(username="w", password="p")
        resp = self.client.post(reverse("core:wallet"), {"amount": "50", "deposit": ""})
        self.assertEqual(resp.status_code, 302)
        wallet = Wallet.objects.get(user=self.user)
        self.assertEqual(wallet.balance, 50)
