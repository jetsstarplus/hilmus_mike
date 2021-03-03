# Generated by Django 3.1.2 on 2021-03-03 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mike_admin', '0012_auto_20210226_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryitem',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='mike_admin.service', verbose_name='category the item belongs to'),
        ),
    ]
