# Generated by Django 4.1.5 on 2023-01-15 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("counter", "0007_btc_data_signal"),
    ]

    operations = [
        migrations.AddField(
            model_name="btc_data",
            name="signal_adx",
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]