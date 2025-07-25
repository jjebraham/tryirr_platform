# core/migrations/0002_add_kyc_fields.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="id_document",
            field=models.FileField(
                upload_to="kyc/id_documents/",
                null=True,
                blank=True,
                help_text="A scan or photo of your government-issued ID.",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="selfie",
            field=models.FileField(
                upload_to="kyc/selfies/",
                null=True,
                blank=True,
                help_text="A selfie of you holding your ID next to your face.",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="proof_of_address",
            field=models.FileField(
                upload_to="kyc/address/",
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="address_document",
            field=models.FileField(
                upload_to="kyc/address/",
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="deposit_proof",
            field=models.FileField(
                upload_to="kyc/deposit/",
                null=True,
                blank=True,
            ),
        ),
        # any other fields you added since 0001_initial…
    ]
