# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# # from django.contrib.auth.models import User
# from .models import Invoice,InvoiceItem
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.conf import settings
# from .views import convert_amount_to_words

# @receiver(post_save, sender=Invoice)
# def invoice_create(sender, instance, created, **kwargs):
#     if created:
#         print("innnnnnnnnnnnnnnnnnnnnnnnnn")
#         user_subject = 'Thank you For purchase From Al-MUMAIZE'
#         print("innnnnnnnnnnnnnnn=======================nnnnnnnnnn")
#         invoiceItem=InvoiceItem.objects.filter(invoice=instance)
#         print(invoiceItem,"innnnnnnnnnnn7777777777777777777777777nnnnnnnnnnnnnn")
#         for i in invoiceItem:
#             print(i,'----------------------this is loooped ----------------------')
#         sub_total = instance.total_amount - instance.vat_total_amount
#         total_amount = instance.total_amount
#         total_amount_words = convert_amount_to_words(total_amount)
#         print("innnnnnnnnnn-----------------------------------nnnnnnnnnnnnnnn")
#         user_message = render_to_string('invoice.html', {'invoice_items': invoiceItem,'invoice':instance,'total_amount_words':total_amount_words,'total_amount':total_amount,'sub_total':sub_total})
#         user_plain_message = strip_tags(user_message)
#         user_from_email = settings.DEFAULT_FROM_EMAIL
#         user_to_email = instance.email
#         send_mail(user_subject, user_plain_message, user_from_email, [user_to_email], html_message=user_message)
