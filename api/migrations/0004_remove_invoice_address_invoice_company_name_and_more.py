# Generated by Django 4.2.4 on 2023-09-02 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_invoice_qr_code_invoice_vat_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='address',
        ),
        migrations.AddField(
            model_name='invoice',
            name='company_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='customer_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]