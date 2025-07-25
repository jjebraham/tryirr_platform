from django.test import TestCase
from django.urls import reverse

from .models import IntegrationSettings


class CoreTests(TestCase):
    def test_home_page_loads(self):
        resp = self.client.get(reverse('core:home'))
        self.assertEqual(resp.status_code, 200)

    def test_integration_settings_crud(self):
        IntegrationSettings.objects.create(
            ghasedak_api_key='x',
            ghasedak_template_name='t',
            mailgrid_api_key='y',
            mailgrid_sender_email='test@example.com',
        )
        obj = IntegrationSettings.objects.get()
        self.assertEqual(obj.ghasedak_api_key, 'x')
        self.assertEqual(obj.mailgrid_sender_email, 'test@example.com')
