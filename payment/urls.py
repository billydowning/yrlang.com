from django.urls import path
from .views import (
    PaymentProcessView, PaymentCancelView,
    PaymentDoneView, PaymentAccountView
)


urlpatterns = [
    path('payment-process', PaymentProcessView.as_view(), name='payment_process'),
    path('payment-done', PaymentDoneView.as_view(), name='payment_done'),
    path('payment-cancel', PaymentCancelView.as_view(), name='payment_cancelled'),
    path('payment-account', PaymentAccountView.as_view(), name='payment_account'),
]
