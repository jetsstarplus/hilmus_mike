# Generated by Django 3.1.2 on 2020-12-18 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daraja', '0014_auto_20201217_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='c2bpaymentmodel',
            name='BillRefNumber',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='c2bpaymentmodel',
            name='BusinessShortCode',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='c2bpaymentmodel',
            name='FirstName',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='c2bpaymentmodel',
            name='InvoiceNumber',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='c2bpaymentmodel',
            name='LastName',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='c2bpaymentmodel',
            name='MSISDN',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='c2bpaymentmodel',
            name='MiddleName',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='c2bpaymentmodel',
            name='ThirdPartyTransID',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='c2bpaymentmodel',
            name='TransID',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='c2bpaymentmodel',
            name='TransTime',
            field=models.CharField(max_length=50),
        ),
    ]
