# Generated by Django 3.1.2 on 2020-11-20 10:39

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20201102_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_summernote.fields.SummernoteTextField(),
        ),
    ]
