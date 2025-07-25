# core/migrations/0003_remove_address_document.py
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_integrationsettings"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="address_document",
        ),
    ]

