# Generated by Django 3.1.2 on 2020-12-10 13:05

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20201203_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_summernote.fields.SummernoteTextField(),
        ),
    ]