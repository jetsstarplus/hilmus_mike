# Generated by Django 3.1.2 on 2020-11-05 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20201101_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='phone',
            field=models.TextField(blank=True, null=True, verbose_name='phone number'),
        ),
    ]
