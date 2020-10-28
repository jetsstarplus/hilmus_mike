# Generated by Django 3.0.3 on 2020-10-27 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='tos',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='avatar'),
        ),
    ]
