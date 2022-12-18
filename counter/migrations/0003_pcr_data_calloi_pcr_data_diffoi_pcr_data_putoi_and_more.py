# Generated by Django 4.0.1 on 2022-12-18 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0002_pcr_data_pcr_data_past'),
    ]

    operations = [
        migrations.AddField(
            model_name='pcr_data',
            name='callOI',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pcr_data',
            name='diffOI',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pcr_data',
            name='putOI',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pcr_data_past',
            name='callOI',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pcr_data_past',
            name='diffOI',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pcr_data_past',
            name='putOI',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
