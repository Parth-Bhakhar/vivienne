# Generated by Django 5.0.6 on 2025-02-19 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_gold_diamond_rate_in_gold_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='diamond',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='silver',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='gold',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
