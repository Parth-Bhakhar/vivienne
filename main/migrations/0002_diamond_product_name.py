# Generated by Django 5.0.6 on 2025-01-21 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diamond',
            name='product_name',
            field=models.CharField(default=2, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
