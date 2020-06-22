from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.shortcuts import render, reverse


# Create your views here.

class PaymentProcessView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = PayPalPaymentsForm
    template_name = 'payment/payment_process.html'

    def test_func(self):
        if self.request.user.groups.filter(name='Professionals').exists():
            return False
        else:
            return True

    def get_initial(self):
        initial = super(PaymentProcessView, self).get_initial()
        host = self.request.get_host()
        initial.update(
            {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': '0.1',
                'item_name': 'Order {}'.format(1),
                'invoice': '1',
                'currency_code': 'INR',
                'notify_url': 'http://{}{}'.format(host,
                                                   reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host,
                                                   reverse('payment_done')),
                'cancel_return': 'http://{}{}'.format(host,
                                                      reverse('payment_cancelled')),
            }

        )
        return initial


class PaymentDoneView(TemplateView):
    template_name = 'payment/payment_done.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentDoneView, self).dispatch(request, *args, **kwargs)


class PaymentCancelView(TemplateView):
    template_name = 'payment/payment_cancel.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentCancelView, self).dispatch( request, *args, **kwargs)