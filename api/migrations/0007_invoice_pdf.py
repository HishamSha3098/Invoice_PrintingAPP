# Generated by Django 4.2.4 on 2023-09-07 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_invoiceitem_amount_alter_invoiceitem_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
    ]
