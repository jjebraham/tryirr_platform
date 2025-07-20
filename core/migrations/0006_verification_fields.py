from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_customuser_id_document_customuser_selfie_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='two_factor_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='deposit_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='proof_of_address',
            field=models.FileField(blank=True, null=True, upload_to='kyc/address_proofs/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='deposit_receipt',
            field=models.FileField(blank=True, null=True, upload_to='kyc/deposit_receipts/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address_country',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address_city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address_zip',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address_street',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.CreateModel(
            name='VerificationSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_api_key', models.CharField(blank=True, max_length=255)),
                ('phone_endpoint', models.CharField(blank=True, max_length=255)),
                ('email_api_key', models.CharField(blank=True, max_length=255)),
                ('email_smtp_server', models.CharField(blank=True, max_length=255)),
            ],
            options={'verbose_name_plural': 'Verification Settings'},
        ),
    ]
