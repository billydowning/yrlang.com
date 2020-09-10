from django.urls import path

from . import views

# Create your urls here.


app_name = 'custom_admin'
urlpatterns = [
    path('invoice-list', views.InvoiceListView.as_view(), name="invoices"),
    path('invoice-list/<int:pk>/', views.InvoiceDetailView.as_view(), name="invoice"),
    path('complains-list/', views.UserComplainListView.as_view(), name="complins_list"),
    path('complains-detail/<int:pk>/', views.UserComplainDetailView.as_view(), name="complain_detail"),
    path('complains-update/<int:pk>/', views.MakeComplainSolveView.as_view(), name="complain_updater_solve"),

]
