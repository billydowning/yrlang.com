from django.urls import path

from . import views

# Create your urls here.


app_name = 'custom_admin'
urlpatterns = [
    path('invoice-list', views.InvoiceListView.as_view(), name="invoices"),
    path('invoice-list/<int:pk>/', views.InvoiceDetailView.as_view(), name="invoice"),
]
