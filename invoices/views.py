# import code; code.interact(local=dict(globals(), **locals()))
from datetime import datetime
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import (CreateView, ListView)
from paypal.standard.forms import PayPalPaymentsForm

from invoices.models import Invoice
from users.models import CustomUser
from .forms import CreateInvoiceForm


class InvoiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "create_invoice.html"
    form_class = CreateInvoiceForm

    def test_func(self):
        return self.request.user.groups.filter(name='Professionals').exists()

    def form_valid(self, form):
        current_user = CustomUser.get(self.request.user.id)
        invoice = form.save(commit=False)
        invoice.payee = current_user
        invoice.payor = form.cleaned_data.get('payor')
        invoice.save()
        messages.success(self.request, 'Your invoice has been created and sent to the client!')
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class Invoices(ListView):
    template_name = "invoices.html"
    context_object_name = "invoices"

    def get_queryset(self):
        query = ""
        current_user = CustomUser.get(self.request.user.id)
        if self.request.user.is_client_user(self.request.session.get('user_role')):
            query = Invoice.objects.filter(payor=current_user)
        elif self.request.user.is_localite_user(self.request.session.get('user_role')):
            query = Invoice.objects.filter(payee=current_user)
        return query


class InvoiceView(LoginRequiredMixin, View):
    template_name = "invoice_checkout.html"
    form_class = PayPalPaymentsForm

    def get(self, request, *args, **kwargs):
        invoice = Invoice.objects.get(id=self.kwargs.get("invoice_id"))
        payee = invoice.payee
        payor = invoice.payor
        host = self.request.get_host()
        initial = (
            {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': '%.2f' % invoice.amount.quantize(Decimal('.01')),
                'item_name': 'Order {}'.format(invoice.id),
                'invoice': '{}'.format(invoice.id),
                'currency_code': 'INR',
                'notify_url': 'http://{}{}'.format(host,
                                                   reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host,
                                                   reverse('payment_done')),
                'cancel_return': 'http://{}{}'.format(host,
                                                      reverse('payment_cancelled')),
            }

        )
        if invoice:
            charge_amount = int(invoice.amount * 100)
            return render(request, self.template_name,
                          {"invoice": invoice,
                           "payee": payee,
                           "payor": payor,
                           "key": settings.STRIPE_KEYS['publishable_key'],
                           'form': self.form_class(initial=initial)})
        return redirect("invoices")


class InvoiceCharge(View):

    def post(self, request, *args, **kwargs):
        invoice = Invoice.objects.get(id=self.kwargs.get("invoice_id"))
        payee = invoice.payee
        payee_account = payee.paymentaccount_set.first()
        if invoice:
            try:
                user = invoice.payor
                stripe.api_key = settings.STRIPE_KEYS.get("secret_key")
                if user.stripe_id is None:
                    customer = stripe.Customer.create(email=user.email,
                                                      description="My First Test Customer (created for API docs)",)
                    ba_acc = stripe.Customer.create_source(
                        customer.id,
                        source=request.POST['stripeToken'],
                    )

                    print('customer', customer)
                    user.stripe_id = customer.id
                    user.save()

                charge = stripe.Charge.create(customer=user.stripe_id, amount=int(invoice.amount * 100), currency='usd',
                                              description=invoice.title)

                payment_intent = stripe.PaymentIntent.create(
                    amount=int(invoice.amount * 100),
                    currency='usd',
                    payment_method_types=['card'],
                    transfer_group=invoice.title,
                )

                transfer = stripe.Transfer.create(
                    amount=int(invoice.amount // 2 * 100),
                    currency='usd',
                    destination=payee_account.account_id,
                    transfer_group=invoice.title,
                )
                # add row in invoices for stripe payment id and store the stripe payment ID from response attribute
                if charge.captured:
                    invoice.is_paid = True
                    invoice.date_paid = datetime.today()
                    invoice.payment_id = charge.id
                    invoice.save()

            except stripe.error.StripeError as e:
                print(e)
                messages.error(request, "Your request to make payment couldn't be processed!")
        messages.success(request, "Your request to make payment processed successfully!")
        return redirect("invoice", invoice_id=invoice.id)
