# Generated by Django 3.0.3 on 2020-10-27 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20201027_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='tos',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
