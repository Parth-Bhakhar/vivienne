# Generated by Django 5.0.6 on 2025-01-28 07:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_metalrate'),
    ]

    operations = [
        migrations.AddField(
            model_name='metalrate',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
