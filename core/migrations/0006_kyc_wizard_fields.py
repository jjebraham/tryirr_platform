from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_customuser_id_document_customuser_selfie_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='country',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_personal_info_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_phone_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_document_uploaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_address_uploaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_deposit_uploaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_verification_code',
            field=models.CharField(max_length=6, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='email_verification_code',
            field=models.CharField(max_length=6, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='proof_of_address',
            field=models.FileField(upload_to='kyc/address/', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='deposit_proof',
            field=models.FileField(upload_to='kyc/deposit/', null=True, blank=True),
        ),
    ]
