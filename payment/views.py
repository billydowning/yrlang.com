from django.shortcuts import render, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, reverse

from .models import PaymentAccount
from .forms import PaymentAccountForm

from paypal.standard.forms import PayPalPaymentsForm



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


class PaymentAccountView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'payment/payment_account.html'
    form_class = PaymentAccountForm

    def test_func(self):
        if self.request.user.is_localite_user(self.request.session.get('user_role')) or \
                self.request.user.is_provider_user(self.request.session.get('user_role')):
            return True
        else:
            return False

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        messages.success(self.request, "Your Payment Account is Added!")
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return super(PaymentAccount, self).form_invalid(form=form)