# Generated by Django 5.0.6 on 2025-01-29 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_silver_diamond_weight_in_silver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gold',
            name='diamond_weight_in_gold',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='silver',
            name='diamond_weight_in_silver',
            field=models.FloatField(),
        ),
    ]
