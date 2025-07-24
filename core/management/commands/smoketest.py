from django.core.management.base import BaseCommand
from django.test import Client


class Command(BaseCommand):
    help = "Simple smoke test visiting key pages"

    def handle(self, *args, **options):
        client = Client()
        urls = [
            '/',
            '/dashboard/',
            '/wallet/',
            '/wallet/deposit/',
            '/wallet/withdraw/',
            '/verification/',
            '/updates/',
        ]
        for url in urls:
            resp = client.get(url)
            if resp.status_code >= 500:
                self.stderr.write(f"❌ {url} returned {resp.status_code}")
            else:
                self.stdout.write(f"✅ {url} -> {resp.status_code}")
