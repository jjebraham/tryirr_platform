from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='balance_tl',
            field=models.DecimalField(default=0, max_digits=12, decimal_places=2),
        ),
        migrations.AddField(
            model_name='customuser',
            name='balance_irr',
            field=models.DecimalField(default=0, max_digits=14, decimal_places=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='balance_usdt',
            field=models.DecimalField(default=0, max_digits=12, decimal_places=2),
        ),
    ]
