from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(
                max_length=20,
                unique=True,
                null=True,
                blank=True,
            ),
        ),
    ]

