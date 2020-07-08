import datetime
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import (DetailView, UpdateView, TemplateView,
                                  FormView, View, ListView, CreateView)
from django.urls import reverse_lazy
#for notification
from webpush import send_user_notification

from allauth.account.views import SignupView
from django.contrib.contenttypes.models import ContentType
from .forms import (
    ProfessionalAccountForm,
    UpdateProfessionalAccountForm,
    UpdateAccountForm,
    UserChoiceForm,
    ClientSignupForm,
    ProfessionalSignupForm,
    ProviderAccountForm,
    UpdateProviderAccountForm,
    ClientToAdminRequestForm
)
from .models import CustomUser, UserRole, UserRoleRequest, UserVideos


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    success_url = '/'

    def test_func(self):
        if self.request.user.is_localite_user(self.request.session.get('user_role')) or \
                self.request.user.is_provider_user(self.request.session.get('user_role')):
            return True
        else:
            return False

    def get_object(self, queryset=None):
        return self.request.user

    def get_template_names(self):
        current_user = self.get_object()
        if self.request.user.is_localite_user(self.request.session.get('user_role')):
            self.template_name = 'localite_profile.html'
            return self.template_name
        elif self.request.user.is_provider_user(self.request.session.get('user_role')):
            self.template_name = 'provider_profile.html'
            return self.template_name

    def get_form(self, form_class=None):
        current_user = self.get_object()
        if self.request.user.is_localite_user(self.request.session.get('user_role')):
            if self.request.method == 'POST':
                self.form_class = ProfessionalAccountForm(
                    instance=current_user,
                    data=self.request.POST,
                    request=self.request
                )
            else:
                self.form_class = ProfessionalAccountForm(instance=current_user, request=self.request)
        else:
            if self.request.method == 'POST':
                self.form_class = ProviderAccountForm(
                    instance=current_user,
                    data=self.request.POST,
                    request=self.request
                )
            else:
                self.form_class = ProviderAccountForm(instance=current_user, request=self.request)
        return self.form_class

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your Profile has been saved successfully!')
        return super(ProfileView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class AccountView(LoginRequiredMixin, UpdateView):
    success_url = '/'

    def get_template_names(self):
        current_user = CustomUser.get(self.request.user.id)
        if self.request.user.is_client_user(self.request.session.get('user_role')):
            self.template_name = "account.html"
            return self.template_name
        elif self.request.user.is_localite_user(self.request.session.get('user_role')):
            self.template_name = "account-professional.html"
            return self.template_name
        elif self.request.user.is_provider_user(self.request.session.get('user_role')):
            self.template_name = "account-provider.html"
            return self.template_name

    def get_form(self, form_class=None):
        self.request.session['role_flag'] = False
        current_user = CustomUser.get(self.request.user.id)
        if self.request.user.is_client_user(self.request.session.get('user_role')):
            if self.request.method == 'POST':
                self.form_class = UpdateAccountForm(
                    instance=current_user,
                    data=self.request.POST,
                    request=self.request
                )
            else:
                self.form_class = UpdateAccountForm(instance=current_user, request=self.request)
        elif self.request.user.is_localite_user(self.request.session.get('user_role')):
            if self.request.method == 'POST':
                self.form_class = UpdateProfessionalAccountForm(
                    instance=current_user,
                    data=self.request.POST,
                    request=self.request
                )
            else:
                self.form_class = UpdateProfessionalAccountForm(instance=current_user, request=self.request)
        elif self.request.user.is_provider_user(self.request.session.get('user_role')):
            if self.request.method == 'POST':
                self.form_class = UpdateProviderAccountForm(
                    instance=current_user,
                    data=self.request.POST,
                    request=self.request
                )
            else:
                self.form_class = UpdateProviderAccountForm(instance=current_user, request=self.request)
        return self.form_class

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        if self.request.session['role_flag'] == UserRole.PROVIDER:
            self.request.session['user_role'] = UserRole.PROVIDER
            self.success_url = reverse_lazy('profile')
        elif self.request.session['role_flag'] == UserRole.LOCALITE:
            self.request.session['user_role'] = UserRole.LOCALITE
            self.success_url = reverse_lazy('profile')
        messages.success(self.request, "User Profile saved successfully!")
        return super(AccountView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'users/user_detail.html'
    model = CustomUser
    context_object_name = 'user'

    def test_func(self):
        return self.request.user.is_client_user(self.request.session.get('user_role'))

    def get_queryset(self):
        return self.model.objects.filter(user_role__name=UserRole.LOCALITE)


class UserMultipleRoleView(TemplateView):
    template_name = "users/user_role.html"

    def get(self, request, *args, **kwargs):
        self.request.session['user_role'] = False
        return super(UserMultipleRoleView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        url = ''
        if self.request.POST.get("role") == UserRole.PROVIDER:
            if self.request.user.phone_number is None \
                    or self.request.user.country is None \
                    or self.request.user.state is None:
                self.request.session['user_role'] = UserRole.PROVIDER
                url = reverse_lazy('profile')
            else:
                self.request.session['user_role'] = UserRole.PROVIDER
                url = '/'
        elif self.request.POST.get("role") == UserRole.LOCALITE:
            if self.request.user.phone_number is None \
                    or self.request.user.country is None \
                    or self.request.user.state is None:
                self.request.session['user_role'] = UserRole.LOCALITE
                url = reverse_lazy('profile')
            else:
                self.request.session['user_role'] = UserRole.LOCALITE
                url = '/'
        elif self.request.POST.get("role") == UserRole.CLIENT:
            self.request.session['user_role'] = UserRole.CLIENT
            url = '/'
        else:
            url = reverse_lazy('account_login')
        return JsonResponse({"url": url})


class ClientSignupView(SignupView):
    form_class = ClientSignupForm
    template_name = 'account/signup.html'

    def form_valid(self, form):
        return super(ClientSignupView, self).form_valid(form)


# Professional Signup View override with allauth SignupView
class ProfessionalSignupView(SignupView):
    form_class = ProfessionalSignupForm
    template_name = 'account/professional_signup.html'


class ProviderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'users/provider_detail.html'
    model = CustomUser
    context_object_name = 'current_user'

    def test_func(self):
        return self.request.user.is_client_user(self.request.session.get('user_role'))

    def get_queryset(self):
        return self.model.objects.filter(user_role__name=UserRole.PROVIDER)


class CreateRequestForProvider(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = ClientToAdminRequestForm
    template_name = 'request_to_admin.html'

    def test_func(self):
        return self.request.user.is_client_user(self.request.session.get('user_role'))

    def get_context_data(self, **kwargs):
        context = super(CreateRequestForProvider, self).get_context_data(**kwargs)
        context['banner'] = 'Request for Provider'
        return context

    def form_valid(self, form):
        role = UserRole.objects.get(name=UserRole.PROVIDER)
        instance = UserRoleRequest.objects.create(user=self.request.user, requested_for=role)
        for each in form.cleaned_data['videos']:
            UserVideos.objects.create(content_object=instance, files=each)
        messages.success(self.request, "Your Request For Become Provider sent Successfully !")
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CreateRequestForLocalite(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = ClientToAdminRequestForm
    template_name = 'request_to_admin.html'

    def test_func(self):
        return self.request.user.is_client_user(self.request.session.get('user_role'))

    def get_context_data(self, **kwargs):
        context = super(CreateRequestForLocalite, self).get_context_data(**kwargs)
        context['banner'] = 'Request for Localite'
        return context

    def form_valid(self, form):
        role = UserRole.objects.get(name=UserRole.LOCALITE)
        instance = UserRoleRequest.objects.create(user=self.request.user, requested_for=role)
        for each in form.cleaned_data['videos']:
            UserVideos.objects.create(content_object=instance, files=each)
        messages.success(self.request, "Your Request For Become Localite sent Successfully !")
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class UserRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'client_request_list.html'
    model = UserRoleRequest
    context_object_name = 'requests'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return self.model.objects.order_by('requested_on').filter(status=UserRoleRequest.REQUESTED)


class AprovedClientRequestView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'client_request_detail.html'
    model = UserRoleRequest
    fields = ['reason']
    context_object_name = 'req'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        req = self.get_object()
        if form.cleaned_data.get("reason"):
            req.status = UserRoleRequest.CANCELED
            form.save()
            req.save()
            messages.success(self.request, "Request Canceled successfully!")
            return HttpResponseRedirect('/')
        else:
            req.status = UserRoleRequest.APPROVED
            req.approved_on = datetime.datetime.now()
            req.save()
            if req.requested_for.name == UserRole.PROVIDER:
                req.user.user_role.add(req.requested_for)
            if req.requested_for.name == UserRole.LOCALITE:
                req.user.user_role.add(req.requested_for)
            messages.success(self.request, "Request Approved successfully!")
            payload_data = {
                "head": "Alert !",
                "body": "Your Request is Accepted."
            }
            send_user_notification(user=req.user, payload=payload_data, ttl=100)
            return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(AprovedClientRequestView, self).get_context_data(**kwargs)
        content_type_obj = ContentType.objects.get_for_model(UserRoleRequest)
        obj = self.get_object()
        context['videos'] = UserVideos.objects.filter(object_id=obj.id, content_type=content_type_obj)
        return context


class VerifyClientRequestView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(UserRoleRequest, pk=self.kwargs.get('id'))
        instance.status = UserRoleRequest.VERIFIED
        instance.save()
        payload_data = {
            "head": "Alert !",
            "body": "Your Request is Verified."
        }
        send_user_notification(user=instance.user, payload=payload_data, ttl=100)
        return redirect('client_request_detail', pk= instance.id)


class PublicProfile(DetailView):
    model = CustomUser
    template_name = 'users/public_profile.html'
    context_object_name = 'user'
