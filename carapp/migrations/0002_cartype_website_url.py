# Generated by Django 5.1.1 on 2024-10-30 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartype',
            name='website_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]