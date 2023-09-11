from django.shortcuts import render,redirect
from .models import Invoice, InvoiceItem
from decimal import Decimal
from django.http import QueryDict
from django.http import JsonResponse
import json
import os
from .utils import generate_qr_code_data
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from num2words import num2words
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
# from xhtml2pdf import pisa 
from django.template.loader import get_template
from io import BytesIO
from django.core.files import File
import imgkit
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags


# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)        
@login_required(login_url='login')
def home(request) :
    print(request.user,'this is user----------------------------------')
    invoice_count = Invoice.objects.count()
    total_amount = Invoice.objects.aggregate(Sum('total_amount'))['total_amount__sum']

    return render(request,"index.html",locals())




@cache_control(no_cache=True,must_revalidate=True,no_store=True)        
def login(request) :
        if request.method == 'POST' :
              username = request.POST['email']
              password = request.POST['password']

              user = auth.authenticate(username=username,password=password)

              if user is not None :
                    auth.login(request,user)
                     
                    print('user logged------------------')
                    messages.success(request,'Welcome Boss')  
                    return redirect(home)
              else :
                    print('user name or password incorrect ---------------------------')
                    messages.error(request,'User name or Password is incorrect')  
                    return redirect(login)
        else :   
              return render(request,"authentication-login.html")

@cache_control(no_cache=True,must_revalidate=True,no_store=True)        
@login_required(login_url='login')       
def invoice_view(request) :
    print(request.user,'this is user----------------------------------')
    invoices = Invoice.objects.all()
    return render(request,"invoice-view.html",locals())

def sent_email(invoice):
        print("innnnnnnnnnnnnnnnnnnnnnnnnn")
        user_subject = 'Thank you For purchase From Al-MUMAIZE'
        invoiceItem=InvoiceItem.objects.filter(invoice=invoice)
        sub_total = invoice.total_amount - invoice.vat_total_amount
        total_amount = invoice.total_amount
        total_amount_words = convert_amount_to_words(total_amount)
        user_message = render_to_string('email--invoice.html', {'invoice_items': invoiceItem,'invoice':invoice,'total_amount_words':total_amount_words,'total_amount':total_amount,'sub_total':sub_total})
        user_plain_message = strip_tags(user_message)
        user_from_email = settings.DEFAULT_FROM_EMAIL
        user_to_email = invoice.email
        send_mail(user_subject, user_plain_message, user_from_email, [user_to_email], html_message=user_message)
        return HttpResponse(status=200)

@cache_control(no_cache=True,must_revalidate=True,no_store=True)        
@login_required(login_url='login')
def create_invoice(request):
    if request.method == 'POST':
        print("im in post method")

        try:
            data = json.loads(request.body)
            print(data)
            # Extract customer details
            customer_name = data.get('customer_name')
            email = data.get('email')
            phone = data.get('phone')
            cust_vat = data.get('cust_vat')
            company_name = data.get('company_name')
            
            # Create the invoice instance
            invoice = Invoice.objects.create(
                customer_name=customer_name,
                email=email,
                phone=phone,
                vat_number=cust_vat,
                company_name=company_name
            )
            
            total_vat = Decimal('0.00')
            total_amounts = Decimal('0.00')

            print("ningal ithuvare puraoettileee")
            # Extract and process items
            for item in data.get('items', []):
                InvoiceItem.objects.create(
                    invoice=invoice,
                    item_code=item['item_code'],
                    description=item['description'],
                    unit=item['unit'],
                    qty=item['qty'],
                    rate=item['rate'],
                    vat_percent=item['vat_percentage'],
                    vat_amount=Decimal(item['vat_amount']),
                    amount=Decimal(item['amount'])
                )
                total_vat += Decimal(item['vat_amount'])
                total_amounts += Decimal(item['amount'])

            invoice.vat_total_amount = total_vat
            invoice.total_amount = total_amounts
            # Generate QR code data
            qr_code_data = f"Invoice Number: {invoice.invoice_number}\n" \
                           f"Company Name: {invoice.company_name}\n" \
                           f"Customer Name: {invoice.customer_name}\n" \
                           f"Total Amount: {invoice.total_amount}\n" \
                           f"Cust-VAT: {invoice.vat_number}"

            qr_code = generate_qr_code_data(qr_code_data)
            invoice.qr_code.save(qr_code.name, qr_code)

            invoice.save()
            sent_email(invoice)

            return redirect('invoice-view')
        
        except:
            print('im heree------------------------')
            print('try not worked')
            messages.success(request,'Invoice Created Successfully')
    
            return redirect('invoice-view')

    return render(request, 'Add_bill.html')
    # return JsonResponse({'message':'sucess'})

def convert_amount_to_words(amount):
    amount_in_words = num2words(amount, lang='en_IN')
    return f"{amount_in_words} Saudi Riyal Only"

# def generate_pdf(html_content):
#     pdf_file = BytesIO()
#     pisa_status = pisa.CreatePDF(BytesIO(html_content.encode("UTF-8")), pdf_file)
#     if pisa_status.err:
#         return None
#     return pdf_file

# from django.conf import settings
# from django.template.loader import get_template
# import imgkit
# import os

# def render_html_to_image(html_content, image_path):
    # options = {
    #     'width': '800',  # Adjust the width as needed
    #     'height': '0',  # Auto-adjust the height
    # }

    # imgkit.from_file(html_content, image_path, options=options)

def invoice_show(request, invoice_number):
    # Fetch the invoice and its details
    invoice = Invoice.objects.get(invoice_number=invoice_number)
    invoice_items = InvoiceItem.objects.filter(invoice=invoice)
    sub_total = invoice.total_amount - invoice.vat_total_amount
    total_amount = invoice.total_amount
    total_amount_words = convert_amount_to_words(total_amount)

#     # Render the HTML to an image

#     # html_content = render_to_string("invoice.html", locals())
#     # image_path = f'invoice_{invoice_number}.png'  # Change the extension to png
#     # render_html_to_image(html_content, image_path)



#     # Save the image to the invoice model
#     # invoice.pdf.save(image_path, ContentFile(open(image_path, 'rb').read()), save=True)

    return render(request, "invoice.html", locals())

# def link_callback(uri, rel):
#     # Convert HTML URIs to absolute system paths for ReportLab to access local images/css
#     if settings.DEBUG:
#         # Development
#         return os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
#     else:
#         # Production
#         return os.path.join(settings.STATIC_ROOT, uri)


def invoice_delete(request,id):
     invoice = Invoice.objects.get(id=id)
     invoice.delete()
     messages.success(request,'invoice deleted successfully')
     return redirect('invoice-view')
     


        
def get_available_years(request):
    available_years = Invoice.objects.dates('date_created', 'year').distinct().order_by('-date_created').values_list('date_created__year', flat=True)
    
    return JsonResponse(list(available_years), safe=False)

def get_yearly_invoice_count(request):
    year = request.GET.get('year')
    
    yearly_invoice_count = Invoice.objects.filter(date_created__year=year).values('date_created__month').annotate(count=Count('id'))
    
    labels = [str(month['date_created__month']) for month in yearly_invoice_count]
    counts = [month['count'] for month in yearly_invoice_count]
    
    return JsonResponse({'labels': labels, 'counts': counts})
          
def logout(request) :
       auth.logout(request)
       print(request.user)
       messages.success(request,'Log Out Successfull')
       return redirect(login)