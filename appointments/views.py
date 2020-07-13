# import code; code.interact(local=dict(globals(), **locals())
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from .forms import ApproveProviderAppointmentForm, ProviderAppointmentCreateForm
from .models import *
from webpush import send_user_notification


class AppoitnemtRequestView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = 'request_appointment.html'

    def test_func(self):
        if self.request.user.is_client_user(self.request.session.get('user_role')) \
                or self.request.user.is_localite_user(self.request.session.get('user_role')):
            return True


class AppointmentView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    template_name = "appointments.html"
    context_object_name = 'bookings'

    def test_func(self):
        if self.request.user.is_client_user(self.request.session.get('user_role')) or\
                self.request.user.is_localite_user(self.request.session.get('user_role')):
            return True

    def get_queryset(self):
        current_user = self.request.user
        query = ""
        if self.request.user.is_client_user(self.request.session.get('user_role')):
            query = Appointment.objects.filter(requestor=current_user).order_by('-date_created')
        elif self.request.user.is_localite_user(self.request.session.get('user_role')):
            query = Appointment.objects.filter(requestee=current_user).order_by('-date_created')
        return query


class NewAppointmentView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Appointment
    template_name = "create_appointment.html"

    def test_func(self):
        return self.request.user.is_localite_user(self.request.session.get('user_role'))

    def get_context_data(self, **kwargs):
        context = super(NewAppointmentView, self).get_context_data()
        context['events'] = Appointment.objects.filter(status=Appointment.CONFIRMED).exclude(id=self.kwargs.get('pk', None))
        return context


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointment_detail.html'


class ProviderAppointmentDetailView(LoginRequiredMixin, DetailView):
    model = ProviderAppointment
    template_name = 'appointment_detail.html'
    context_object_name = 'appointment'

    def get_context_data(self, **kwargs):
        context = super(ProviderAppointmentDetailView, self).get_context_data()
        context['appointments'] = self.get_queryset()
        return context


class ProviderAppointmentCreateView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = 'provider_create_appointment.html'

    def test_func(self):
        return self.request.user.is_client_user(self.request.session.get('user_role'))

    def get_context_data(self, **kwargs):
        context = super(ProviderAppointmentCreateView, self).get_context_data()
        context['appointments'] = ProviderAppointment.objects.filter(
            requestee=CustomUser.get(id=self.kwargs.get('pk', None))
        )
        return context


class ProviderAppointmentList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "provider_appointment_list.html"
    context_object_name = 'appointments'

    def test_func(self):
        if self.request.user.is_client_user(self.request.session.get('user_role')) or\
                self.request.user.is_provider_user(self.request.session.get('user_role')):
            return True

    def get_queryset(self):
        current_user = self.request.user
        query = ""
        if self.request.user.is_client_user(self.request.session.get('user_role')):
            query = ProviderAppointment.objects.filter(requestor=current_user,
                                                       ).order_by('-created_date')
        elif self.request.user.is_provider_user(self.request.session.get('user_role')):
            query = ProviderAppointment.objects.filter(requestee=current_user,
                                                       ).order_by('-created_date')
        return query


class EditProviderAppointmentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'provider_create_appointment.html'
    form_class = ProviderAppointmentCreateForm
    model = ProviderAppointment
    context_object_name = 'appoientment'

    def test_func(self):
        appointment = self.get_object()
        if appointment.requestor == self.request.user:
            return True
        else:
            return False

    def form_valid(self, form):
        form.save()
        messages.success(self.request,
                         'Your appointment request has been Updated')
        return redirect('provider_appointment')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CancelAppointmnetView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProviderAppointment
    success_url = reverse_lazy('provider_appointment')

    def test_func(self):
        appointment = self.get_object()
        if appointment.requestor == self.request.user:
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        messages.success(self.request,
                         'Your appointment request has been Delated')
        return self.post(request, *args, **kwargs)


class SaveBookings(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs2):
        localite = request.POST.get('localite', None)
        booking_id = request.POST.get('booking_id', None)

        if localite:
            booking_data = request.POST.getlist('booking_data[]', [])
            data = [json.loads(item) for item in booking_data]
            requestor = self.request.user
            requestee = CustomUser.objects.get(id=localite)
            booking = Appointment.objects.create(requestor=requestor, requestee=requestee)
            payload_data = {
                "head": 'Yr-lang',
                "body": "You have an Booking from " + booking.requestor.email,
                "icon": "https://i0.wp.com/yr-lang.com/wp-content/uploads/2019/12/YRLANGBLACK.png?fit=583%2C596&ssl=1"
            }
            send_user_notification(user=booking.requestee, payload=payload_data, ttl=100)

            for obj in data:
                BookingDates.objects.create(booking=booking, date=obj['date'], start_time=obj['start'], end_time=obj['end'])

            url = reverse('request_appointment', args=[localite])

        if booking_id:
            flag = request.POST.get('flag', None)
            note = request.POST.get('note', None)

            if flag == 'true':
                booking = Appointment.objects.get(id=booking_id)
                booking.notes = note
                booking.status = Appointment.CONFIRMED
                booking.save()

            if flag == 'false':
                booking = Appointment.objects.get(id=booking_id)
                booking.notes = note
                booking.status = Appointment.CANCELED
                booking.save()

            url = reverse_lazy('appointments')
        return JsonResponse({'url': url})

class SaveAppointments(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs2):
        provider = request.POST.get('provider', None)
        appointment_id = request.POST.get('appointment_id', None)

        if provider:
            data = json.loads(request.POST.get('obj', None))
            form = ProviderAppointmentCreateForm(data=data)
            if form.is_valid:
                instance = form.save(commit=False)
                instance.requestee_id = provider
                instance.requestor_id = self.request.user.id
                instance.save()
                payload_data = {
                    "head": 'Yr-lang',
                    "body": "You have an appointment from " + instance.requestor.email ,
                    "icon": "https://i0.wp.com/yr-lang.com/wp-content/uploads/2019/12/YRLANGBLACK.png?fit=583%2C596&ssl=1"
                }
                send_user_notification(user=instance.requestee, payload=payload_data, ttl=100)



        if appointment_id:
            appointment = ProviderAppointment.objects.get(id=appointment_id)
            data = json.loads(request.POST.get('obj', None))
            flag = request.POST.get('flag', None)

            if flag == 'true':
                data['status'] = True
                form = ApproveProviderAppointmentForm(instance=appointment, data=data)
                if form.is_valid():
                    form.save()

            if flag == 'false':
                data['status'] = False
                form = ApproveProviderAppointmentForm(instance=appointment, data=data)
                if form.is_valid():
                    form.save()

        url = reverse_lazy('provider_appointment')

        return JsonResponse({'url': url})
