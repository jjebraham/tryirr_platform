from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_remove_customuser_address_document"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="two_factor_enabled",
            field=models.BooleanField(default=False),
        ),
    ]
