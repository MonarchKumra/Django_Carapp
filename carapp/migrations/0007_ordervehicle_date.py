# Generated by Django 5.1.3 on 2024-11-20 23:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0006_alter_buyer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordervehicle',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]