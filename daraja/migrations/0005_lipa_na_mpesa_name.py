# Generated by Django 3.0.3 on 2020-07-17 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daraja', '0004_lipa_na_mpesa'),
    ]

    operations = [
        migrations.AddField(
            model_name='lipa_na_mpesa',
            name='name',
            field=models.CharField(default='Name', max_length=256),
            preserve_default=False,
        ),
    ]
