from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_customuser_id_document_customuser_selfie_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address_country',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address_city',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address_zip',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address_street',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address_document',
            field=models.FileField(upload_to='kyc/address/', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='deposit_proof',
            field=models.FileField(upload_to='kyc/deposit/', null=True, blank=True),
        ),
    ]
