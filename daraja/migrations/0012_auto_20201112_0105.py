# Generated by Django 3.1.2 on 2020-11-11 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daraja', '0011_initiate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='initiate',
            options={'verbose_name': 'Initiated Transaction', 'verbose_name_plural': 'Initiated Transactions'},
        ),
        migrations.AddField(
            model_name='initiate',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
