# Generated by Django 4.2.4 on 2023-09-06 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_invoice_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='amount',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='rate',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='vat_amount',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]