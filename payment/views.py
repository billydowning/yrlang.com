from django.shortcuts import render, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View, TemplateView, CreateView
from django.contrib.auth.mixins import  UserPassesTestMixin
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, reverse
from django.urls import reverse_lazy

from customemixing.session_and_login_mixing import UserSessionAndLoginCheckMixing
from .models import PaymentAccount, StripeKeys
from .forms import PaymentAccountForm

from paypal.standard.forms import PayPalPaymentsForm
import stripe



# Create your views here.

class PaymentProcessView(UserSessionAndLoginCheckMixing, UserPassesTestMixin, FormView):
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


class PaymentAccountView(UserSessionAndLoginCheckMixing, UserPassesTestMixin, CreateView):
    template_name = 'payment/payment_account.html'
    form_class = PaymentAccountForm

    def test_func(self):
        if self.request.user.is_localite_user(self.request.session.get('user_role')) or \
                self.request.user.is_provider_user(self.request.session.get('user_role')):
            return True
        else:
            return False

    def form_valid(self, form):
        # stripe.api_key = settings.STRIPE_KEYS['secret_key']
        stripe.api_key = StripeKeys.objects.get(is_active=True).secret_key
        post = form.save(commit=False)
        country = form.cleaned_data['country']
        currency = form.cleaned_data['currency']
        account_holder_name = form.cleaned_data['account_holder_name']
        account_holder_type = form.cleaned_data['account_holder_type']
        account_number = form.cleaned_data['account_number']
        account = stripe.Account.create(
            type="custom",
            country=country,
            email=self.request.user.email,
            requested_capabilities=[
                "card_payments",
                "transfers",
            ],
        )
        account_link = stripe.AccountLink.create(
          account=account.id,
          refresh_url="http://127.0.0.1:8000/",
          return_url="http://127.0.0.1:8000/",
          type="custom_account_verification",
        )
        ex_acc = stripe.Account.create_external_account(
            account.id,
            external_account={
                "object": "bank_account",
                "country": country,
                "currency": currency,
                "account_holder_name": account_holder_name,
                "account_holder_type": account_holder_type,
                "routing_number": "110000000",
                "account_number": account_number,
            },
        )
        retrieve_acc = stripe.Account.retrieve(account.id)
        post.user = self.request.user
        post.routing_number = '110000000'
        post.account_id = account.id
        post.account_link = account_link['url']
        post.account_status = retrieve_acc['details_submitted']
        post.save()
        messages.success(self.request, "Your Payment Account is Added!")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):

        return reverse_lazy('payment_account')

    def form_invalid(self, form):
        return super(PaymentAccount, self).form_invalid(form=form)

    def get_context_data(self, **kwargs):
        context = super(PaymentAccountView, self).get_context_data()
        return context
