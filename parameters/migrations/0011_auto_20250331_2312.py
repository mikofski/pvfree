# Generated by Django 2.2.28 on 2025-04-01 06:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0010_pvinverter_sam_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pvinverter',
            name='CEC_Date',
            field=models.DateField(default=datetime.datetime(1990, 1, 1, 0, 0)),
        ),
    ]
