from django.urls import path

from . import views

urlpatterns = [
    path('create-invoice', views.InvoiceCreateView.as_view(), name="create_invoice"),
    path('create-invoice/<int:object_id>', views.InvoiceCreateView.as_view(), name="create-invoice"),
    path('provider-create-invoice', views.ProviderInvoiceCreateView.as_view(), name="provider_create_invoice"),
    path('provider-create-invoice/<int:object_id>', views.ProviderInvoiceCreateView.as_view(), name="provider_create_invoice_with_id"),
    path('invoices', views.Invoices.as_view(), name="invoices"),
    path('invoice/<int:invoice_id>', views.InvoiceView.as_view(), name="invoice"),
    path('charge/<int:invoice_id>', views.InvoiceCharge.as_view(), name="charge"),
    path('create-checkout-session/<int:invoice_id>/', views.CreateCheckoutSession.as_view(), name="checkout"),
    path('create-checkout-session', views.CreateCheckoutSession.as_view(), name="checkout"),
    path('checkout-capture/', views.WebHook.as_view(), name="checkout_capture"),
    path('invoice-pdf/<pk:invoice_id>', views.InvoicePdfView.as_view(), name="checkout_capture"),
]