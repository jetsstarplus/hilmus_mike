# Generated by Django 3.1.2 on 2021-02-26 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mike_admin', '0011_categoryitem_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoryitem',
            old_name='Image',
            new_name='image',
        ),
    ]
