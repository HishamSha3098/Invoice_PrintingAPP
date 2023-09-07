from django.urls import path
from .import views
# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login,name="login"),
    path('invoice-view/',views.invoice_view,name="invoice-view"),
    # path('add-bill',views.add_bill,name="addbill"),
    path('create-invoice',views.create_invoice,name="create-invoice"),
    path('delete-invoice/<int:id>/',views.invoice_delete,name="delete-invoice"),
    path('invoice/<str:invoice_number>/', views.invoice_show, name='invoice'),
     path('get_available_years/', views.get_available_years, name='get_available_years'),
    path('get_yearly_invoice_count/', views.get_yearly_invoice_count, name='get_yearly_invoice_count'),
    path('logout/', views.logout, name='logout'),

]
