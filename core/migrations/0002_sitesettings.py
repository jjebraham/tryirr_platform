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
                ('telegram_bot_token', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'Site settings',
                'verbose_name_plural': 'Site settings',
            },
        ),
    ]
