# Generated by Django 3.1.2 on 2021-03-03 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0016_post_read_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visit',
            field=models.IntegerField(default=0, verbose_name='Number of Visits'),
        ),
    ]
