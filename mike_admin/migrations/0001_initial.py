# Generated by Django 3.1.2 on 2020-11-05 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsOfService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='testimonials')),
                ('is_published', models.BooleanField(default=False)),
                ('content', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=15)),
                ('rank', models.IntegerField(default=1)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='testimonials')),
                ('is_published', models.BooleanField(default=False)),
                ('facebook', models.CharField(blank=True, max_length=50, null=True)),
                ('twitter', models.CharField(blank=True, max_length=50, null=True)),
                ('instagram', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='More Information')),
                ('title', models.CharField(max_length=30)),
                ('music', models.FileField(upload_to='Musics')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='Music-pics')),
                ('is_sent', models.BooleanField(default=False, verbose_name='Has been sent')),
                ('is_boompay', models.BooleanField(default=True, verbose_name='To upload to boomplay')),
                ('is_skiza', models.BooleanField(blank=True, default=False, null=True, verbose_name='Generate the skiza code')),
                ('skiza_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='The generated Skiza Code')),
                ('seo_title', models.CharField(blank=True, max_length=50, null=True)),
                ('seo_description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('artist', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='musics', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
