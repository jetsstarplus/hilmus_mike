# Generated by Django 3.1.2 on 2021-02-26 13:13

from django.db import migrations, models
import django.db.models.deletion
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mike_admin', '0009_auto_20210103_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(blank=True, null=True, upload_to='categoryItemImages', verbose_name='Item Image')),
                ('PDF', models.FileField(blank=True, upload_to='categoryItemPdf', verbose_name='Category Item Pdf')),
                ('content', django_summernote.fields.SummernoteTextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mike_admin.service', verbose_name='category the item belongs to')),
            ],
        ),
    ]