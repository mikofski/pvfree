# Generated by Django 2.2.28 on 2025-04-01 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0011_auto_20250331_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cec_module',
            name='Version',
            field=models.IntegerField(blank=True, choices=[(0, ''), (1, 'MM105'), (2, 'MM106'), (3, 'MM107'), (4, 'NRELv1'), (5, 'SAM 2018.9.27'), (6, 'SAM 2018.10.29'), (7, 'SAM 2018.11.11'), (8, 'SAM 2018.11.11 r2'), (9, 'SAM 2019.12.19'), (10, 'SAM 2020.2.29 r3'), (11, 'SAM 2021.12.02'), (12, 'SAM 2023.10.31'), (13, 'SAM 2023.12.17')], default=0),
        ),
    ]
