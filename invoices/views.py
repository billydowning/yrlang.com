# import code; code.interact(local=dict(globals(), **locals()))
import logging
from datetime import datetime
from decimal import Decimal
import stripe
from django.core import exceptions
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import (CreateView, ListView, DetailView)
from paypal.standard.forms import PayPalPaymentsForm

from customemixing.session_and_login_mixing import UserSessionAndLoginCheckMixing
from invoices.models import Invoice
from users.models import CustomUser
from .forms import CreateInvoiceForm, ProviderCreateInvoiceForm
from appointments.models import Appointment, ProviderAppointment
from payment.models import Commission, StripeKeys

# logger = logging.getLogger(__name__)


class InvoiceCreateView(UserSessionAndLoginCheckMixing, UserPassesTestMixin, CreateView):
    template_name = "create_invoice.html"
    form_class = CreateInvoiceForm

    def test_func(self):
        return self.request.user.groups.filter(name='Professionals').exists()

    def form_valid(self, form):
        current_user = CustomUser.get(self.request.user.id)
        invoice = form.save(commit=False)
        invoice.payee = current_user
        booking = form.cleaned_data.get('booking')
        invoice.payor = booking.requestor
        invoice.save()
        messages.success(self.request, 'Your invoice has been created and sent to the client!')
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_form_kwargs(self, **kwargs):
        kwargs = super(InvoiceCreateView, self).get_form_kwargs(**kwargs)
        kwargs['user'] = self.request.user
        kwargs['object_id'] = self.kwargs.get('object_id')
        return kwargs

class ProviderInvoiceCreateView(UserSessionAndLoginCheckMixing, UserPassesTestMixin, CreateView):
    template_name = "provider_create_invoice.html"
    form_class = ProviderCreateInvoiceForm

    def test_func(self):
        return self.request.user.groups.filter(name='Professionals').exists()

    def form_valid(self, form):
        current_user = CustomUser.get(self.request.user.id)
        invoice = form.save(commit=False)
        invoice.payee = current_user
        appointment = form.cleaned_data.get('appointment')
        invoice.payor = appointment.requestor
        invoice.save()
        messages.success(self.request, 'Your invoice has been created and sent to the client!')
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ProviderInvoiceCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['object_id'] = self.kwargs.get('object_id')
        return kwargs


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
        elif self.request.user.is_provider_user(self.request.session.get('user_role')):
            query = Invoice.objects.filter(payee=current_user)
        return query


class InvoiceView(UserSessionAndLoginCheckMixing, View):
    template_name = "invoice_checkout.html"
    form_class = PayPalPaymentsForm

    def get(self, request, *args, **kwargs):
        try:
            invoice = Invoice.objects.get(id=self.kwargs.get("invoice_id"))
        except exceptions.ObjectDoesNotExist as e:
            print("Invoice Object Not Exist\n", e)

        payee = invoice.payee
        payor = invoice.payor
        host = self.request.get_host()
        try:
            key = StripeKeys.objects.get(is_active=True).publishable_key
        except exceptions.ObjectDoesNotExist as e:
            print("StripeKeys publishable_key Not Exist\n", e)
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
            return render(
                request, self.template_name,
                {
                    "invoice": invoice,
                    "payee": payee,
                    "payor": payor,
                    "key": key,
                    'form': self.form_class(initial=initial)
                }
            )
        return redirect("invoices")


class InvoiceCharge(View):

    def post(self, request, *args, **kwargs):
        invoice = Invoice.objects.get(id=self.kwargs.get("invoice_id"))
        payee = invoice.payee
        payee_account = payee.paymentaccount_set.first()
        if invoice:
            try:
                user = invoice.payor
                # stripe.api_key = settings.STRIPE_KEYS.get("secret_key")
                stripe.api_key = StripeKeys.objects.get(is_active=True).secret_key
                if user.stripe_id is None:
                    customer = stripe.Customer.create(email=user.email,
                                                      description="My First Test Customer (created for API docs)", )
                    ba_acc = stripe.Customer.create_source(
                        customer.id,
                        source=request.POST['stripeToken'],
                    )
                    user.stripe_id = customer.id
                    user.save()

                charge = stripe.Charge.create(customer=user.stripe_id, amount=int(invoice.amount * 100), currency='usd',
                                              description=invoice.title)
                if charge.captured:
                    invoice.is_paid = True
                    invoice.date_paid = datetime.today()
                    invoice.payment_id = charge.id
                    if invoice.booking:
                        invoice.booking.status = Appointment.COMPLETED
                    elif invoice.appointment:
                        invoice.appointment.status = ProviderAppointment.COMPLETED
                    invoice.save()

                payment_intent = stripe.PaymentIntent.create(
                    amount=int(invoice.amount * 100),
                    currency='usd',
                    payment_method_types=['card'],
                    transfer_group=invoice.title,
                )
                if invoice.booking:
                    commission = Commission.objects.get(
                        Professional=Commission.LOCALITE,
                        is_active=True
                    ).percentage
                    amount = invoice.amount // commission
                elif invoice.appointment:
                    commission = Commission.objects.get(
                        Professional=Commission.PROVIDER,
                        is_active=True
                    ).percentage
                    amount = invoice.amount // commission
                else:
                    amount = invoice.amount

                transfer = stripe.Transfer.create(
                    amount=int(amount * 100),
                    currency='usd',
                    destination=payee_account.account_id,
                    transfer_group=invoice.title,
                )
                # add row in invoices for stripe payment id and store the stripe payment ID from response attribute

            except stripe.error.StripeError as e:
                print(e)
                # messages.error(request, "Your request to make payment couldn't be processed!")
        messages.success(request, "Your request to make payment processed successfully!")
        return redirect("invoice", invoice_id=invoice.id)


class CreateCheckoutSession(View):
    def get(self, request, *args, **kwargs):
        stripe.api_key = StripeKeys.objects.get(is_active=True).secret_key
        stripe_pk = StripeKeys.objects.get(is_active=True).publishable_key
        invoice_id = self.kwargs.get("invoice_id", None)
        e = 'StripeKeys secret_key Not Exist'
        # logger.error(self.__class__.__name__+" \n      ->"+e)

        return render(request, 'checkout.html', {'stripe_pk': stripe_pk, 'invoice_id': invoice_id})

    def post(self, request, *args, **kwargs):
        invoice_id = request.POST.get('invoice_id', None)

        try:
            stripe.api_key = StripeKeys.objects.get(is_active=True).secret_key
        except exceptions.ObjectDoesNotExist as e:
            print("StripeKeys secret_key Not Exist\n", e)

        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except exceptions.ObjectDoesNotExist as e:
            print("Invoice Is Not Exist\n", e)

        try:
            customer_id = Invoice.objects.get(id=invoice_id).payor.stripe_id
        except exceptions.ObjectDoesNotExist as e:
            customer_id = None

        if customer_id:
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': invoice.title,
                        },
                        'unit_amount': int(invoice.amount),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                metadata={
                    'invoice_id': str(invoice_id),
                },
                success_url='http://yrlang.com/checkout-capture/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://yrlang.com/checkout-capture/',
            )
        else:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': invoice.title,
                        },
                        'unit_amount': int(invoice.amount * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                metadata={
                    'invoice_id': str(invoice_id),
                },
                success_url='http://yrlang.com/checkout-capture/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://yrlang.com/checkout-capture/',
            )
        return JsonResponse({'id': session.id})


class InvoicePdfView(DetailView):
    template_name = 'invoice_pdf.html'
    model = Invoice
    context_object_name = "invoice"


class WebHook(View):
    def get(self, request):
        session_id = request.GET['session_id']
        try:
            stripe.api_key = StripeKeys.objects.get(is_active=True).secret_key
        except exceptions.ObjectDoesNotExist as e:
            print("StripeKeys secret_key Not Exist\n", e)

        ses_re = stripe.checkout.Session.retrieve(
            session_id,
        )

        if ses_re.metadata:
            invoice_id = ses_re.metadata.invoice_id
            try:
                invoice = Invoice.objects.get(id=invoice_id)
            except exceptions.ObjectDoesNotExist as e:
                print("Invoice Object Not Exist\n |->", e)

            if ses_re.payment_status == 'paid':
                invoice.is_paid = True
                invoice.date_paid = datetime.today()
                invoice.payment_id = session_id
                if invoice.booking:
                    invoice.booking.status = Appointment.COMPLETED
                elif invoice.appointment:
                    invoice.appointment.status = ProviderAppointment.COMPLETED
                invoice.save()

        else:
            if ses_re.payment_status == 'paid':
                raise AttributeError('stripe session metadata is None Payment is Paid')
            else:
                raise AttributeError('stripe session metadata is None Payment is Not Paid')

        return redirect("invoice", invoice_id=invoice.id)
