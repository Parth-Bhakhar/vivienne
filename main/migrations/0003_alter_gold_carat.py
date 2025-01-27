# Generated by Django 5.0.6 on 2025-01-27 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_diamond_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gold',
            name='carat',
            field=models.FloatField(choices=[(91.6, '22K'), (84.0, '20K'), (76.0, '18K'), (58.33, '14K')]),
        ),
    ]
