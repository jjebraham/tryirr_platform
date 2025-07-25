from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_remove_address_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ghasedak_api_key', models.CharField(blank=True, max_length=255)),
                ('ghasedak_template_name', models.CharField(blank=True, max_length=255)),
                ('mailgrid_api_key', models.CharField(blank=True, max_length=255)),
                ('mailgrid_sender', models.EmailField(blank=True, max_length=254)),
            ],
        ),
    ]
