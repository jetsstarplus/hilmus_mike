# Generated by Django 3.0.3 on 2020-10-27 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('b8c40c95-3e42-4d4c-8aa6-cc51cf43a28b'), primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True, verbose_name='More Information')),
                ('title', models.CharField(max_length=30)),
                ('music', models.FileField(upload_to='Musics')),
                ('picture', models.ImageField(upload_to='Music-pics')),
                ('is_sent', models.BooleanField(default=False, verbose_name='Has been sent')),
                ('is_boompay', models.BooleanField(default=True, verbose_name='To upload to boomplay')),
                ('is_skiza', models.BooleanField(blank=True, default=False, null=True, verbose_name='Generate the skiza code')),
                ('seo_title', models.CharField(blank=True, max_length=50, null=True)),
                ('seo_description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('artist', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
