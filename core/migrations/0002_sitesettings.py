from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sendgrid_api_key', models.CharField(max_length=255, blank=True)),
                ('sms_api_key', models.CharField(max_length=255, blank=True)),
                ('telegram_api_key', models.CharField(max_length=255, blank=True)),
                ('dark_mode_enabled', models.BooleanField(default=True)),
            ],
        ),
    ]

