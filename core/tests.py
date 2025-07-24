from django.test import TestCase
from django.urls import reverse

from .models import SiteSettings, CustomUser


class SiteSettingsTest(TestCase):
    def test_singleton_load(self):
        s1 = SiteSettings.load()
        s1.sendgrid_api_key = 'abc'
        s1.save()
        s2 = SiteSettings.load()
        self.assertEqual(s2.sendgrid_api_key, 'abc')


class WalletEndpointsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='u', password='p')
        self.client.login(username='u', password='p')

    def test_wallet_views(self):
        for url in [reverse('core:wallet'), reverse('core:wallet_deposit'), reverse('core:wallet_withdraw')]:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)
