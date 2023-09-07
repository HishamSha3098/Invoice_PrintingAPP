from django.db import models

import random

class Invoice(models.Model):
    invoice_number = models.CharField(unique=True)
    date_created = models.DateField(auto_now_add=True)
    customer_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=20,null=True,blank=True)
    company_name = models.CharField(max_length=150,null=True,blank=True)
    vat_number = models.CharField(max_length=150,null=True, blank=True)
    vat_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    pdf = models.FileField(upload_to='files/',null=True,blank=True)

    def generate_invoice_number(self):
        return str(random.randint(100, 100000))  # Generate a random 3-digit number

    def save(self, *args, **kwargs):
        if not self.invoice_number:  # Check if the invoice number is not set
            self.invoice_number = self.generate_invoice_number()  # Generate invoice number
        # self.vat_total_amount = sum(item.vat_amount for item in self.invoice_items.all())
        # self.total_amount = sum(item.amount for item in self.invoice_items.all()) + self.vat_total_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoice_items', on_delete=models.CASCADE)
    item_code = models.CharField(max_length=20)
    description = models.TextField()
    unit = models.CharField(max_length=10)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=3)
    vat_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    

    # def save(self, *args, **kwargs):
    #     self.vat_amount = (self.qty * self.rate * self.vat_percent) / 100
    #     self.amount = self.qty * self.rate + self.vat_amount
    #     super(InvoiceItem, self).save(*args, **kwargs)
