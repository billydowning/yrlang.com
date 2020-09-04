import datetime
from _collections import defaultdict
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import (DetailView, UpdateView, TemplateView,
                                  FormView, View, ListView, CreateView, RedirectView)
from yrlang.settings import development_example
from django.urls import reverse_lazy
from django.core.mail import send_mail
# for notification
from webpush import send_user_notification
from django.forms import formset_factory

from allauth.account.views import SignupView
import stripe
from customemixing.session_and_login_mixing import UserSessionAndLoginCheckMixing

from .forms import (
    ProfessionalAccountForm,
    UpdateProfessionalAccountForm,
    UpdateAccountForm,
    UserChoiceForm,
    ClientSignupForm,
    ProfessionalSignupForm,
    ProviderAccountForm,
    UpdateProviderAccountForm,
    RequestVerificationForm,
    ClientToAdminRequestFormSet

)
from .models import CustomUser, UserRole, UserRoleRequest, UserVideos, UserFavorite
from payment.models import PaymentAccount

from blogpost.models.city_page import CityPage
class ProfileView(UserSessionAndLoginCheckMixing, UserPassesTestMixin, UpdateView):
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


class AccountView(UserSessionAndLoginCheckMixing, UpdateView):
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        accounts = PaymentAccount.objects.filter(user=request.user)

        for account in accounts:
            if account.account_status == "False":
                stripe.api_key = settings.STRIPE_KEYS['secret_key']
                retrieve_acc = stripe.Account.retrieve(account.account_id)
                account.account_status = retrieve_acc['details_submitted']
                account.save()
        return super(AccountView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        current_user = CustomUser.get(self.request.user.id)
        if self.request.user.is_client_user(
                self.request.session.get('user_role')) or self.request.user.is_language_verifier_user(
            self.request.session.get('user_role')):
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
        if self.request.user.is_client_user(
                self.request.session.get('user_role')) or self.request.user.is_language_verifier_user(
            self.request.session.get('user_role')):
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


class UserDetailView(UserSessionAndLoginCheckMixing, UserPassesTestMixin, DetailView):
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
        elif self.request.POST.get("role") == UserRole.LANGUAGE_VERIFIER:
            self.request.session['user_role'] = UserRole.LANGUAGE_VERIFIER
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


class ProviderDetailView(UserSessionAndLoginCheckMixing, UserPassesTestMixin, DetailView):
    template_name = 'users/provider_detail.html'
    model = CustomUser
    context_object_name = 'current_user'

    def test_func(self):
        return self.request.user.is_client_user(self.request.session.get('user_role'))

    def get_queryset(self):
        return self.model.objects.filter(user_role__name=UserRole.PROVIDER)


class CreateRequestForProvider(UserSessionAndLoginCheckMixing, UserPassesTestMixin, FormView):
    form_class = ClientToAdminRequestFormSet
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
        for frm in form:
            form_instance = frm.save(commit=False)
            form_instance.content_object = instance
            form_instance.save()
        # for each in form.cleaned_data['videos']:
        #     UserVideos.objects.create(content_object=instance, files=each)
        messages.success(self.request, "Your Request For Become Provider sent Successfully !")
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CreateRequestForLocalite(UserSessionAndLoginCheckMixing, UserPassesTestMixin, FormView):
    form_class = ClientToAdminRequestFormSet
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
        for frm in form:
            form_instance = frm.save(commit=False)
            form_instance.content_object = instance
            form_instance.save()
        # for each in form.cleaned_data['videos']:
        #     UserVideos.objects.create(content_object=instance, files=each)
        messages.success(self.request, "Your Request For Become Localite sent Successfully !")
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class UserRequestListView(UserSessionAndLoginCheckMixing, UserPassesTestMixin, ListView):
    template_name = 'client_request_list.html'
    model = UserRoleRequest
    context_object_name = 'requests'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_language_verifier_user(
            self.request.session.get('user_role'))

    def get_queryset(self):
        if self.request.user.is_staff:
            return None
        else:
            return self.model.objects.order_by('requested_on').filter(
                status__in=[UserRoleRequest.REQUESTED, UserRoleRequest.VERIFIED, UserRoleRequest.APPROVED],
            ).exclude(user=self.request.user)


class AprovedClientRequestView(UserSessionAndLoginCheckMixing, UserPassesTestMixin, UpdateView):
    template_name = 'client_request_detail.html'
    model = UserRoleRequest
    form_class = RequestVerificationForm
    context_object_name = 'req'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_language_verifier_user(
            self.request.session.get('user_role'))

    def form_valid(self, form):
        req = self.get_object()
        if form.cleaned_data.get("reason"):
            req.status = UserRoleRequest.CANCELED
            form.save()
            req.save()
            messages.success(self.request, "Request Canceled successfully!")
            return HttpResponseRedirect('/')
        else:
            meeting_date = form.cleaned_data.get('meeting_on')
            req.status = UserRoleRequest.APPROVED
            req.approved_on = datetime.datetime.now()
            req.meeting_on = meeting_date
            req.save()
            if req.requested_for.name == UserRole.PROVIDER:
                req.user.user_role.add(req.requested_for)
            elif req.requested_for.name == UserRole.LOCALITE:
                req.user.user_role.add(req.requested_for)
            elif req.requested_for.name == UserRole.LANGUAGE_VERIFIER:
                req.user.user_role.add(req.requested_for)
            messages.success(self.request, "Request Approved successfully!")
            payload_data = {
                "head": "YR-lang",
                "body": "Your Request is Accepted For " + req.requested_for.name,
                "icon": "https://i0.wp.com/yr-lang.com/wp-content/uploads/2019/12/YRLANGBLACK.png?fit=583%2C596&ssl=1"
            }
            send_user_notification(user=req.user, payload=payload_data, ttl=100)
            send_mail(
                'Request Approved for ' + req.requested_for.name,
                'Your Request is Approved for ' + req.requested_for.name + '',
                development_example.EMAIL_HOST_USER,
                [str(req.user.email)],
                fail_silently=True,
            )
            return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AprovedClientRequestView, self).get_form_kwargs(**kwargs)
        kwargs['model_object'] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AprovedClientRequestView, self).get_context_data(**kwargs)
        content_type_obj = ContentType.objects.get_for_model(UserRoleRequest)
        obj = self.get_object()
        context['videos'] = UserVideos.objects.filter(object_id=obj.id, content_type=content_type_obj)
        results = UserRoleRequest.objects.values('meeting_on').all().exclude(id=obj.id).exclude(meeting_on=None)
        date_dict = defaultdict(list)
        for date_l in results:
            date_dict[str(date_l['meeting_on'].date().strftime("%Y.%m.%d"))].append(
                str(date_l['meeting_on'].time().strftime("%H:%M")))
        context['disabled_dates'] = dict(date_dict)
        return context


class VerifyClientRequestView(UserSessionAndLoginCheckMixing, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_language_verifier_user(
            self.request.session.get('user_role'))

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(UserRoleRequest, pk=self.kwargs.get('id'))
        instance.status = UserRoleRequest.VERIFIED
        instance.save()
        payload_data = {
            "head": "YR-lang",
            "body": "Your Request is Verified  for " + instance.requested_for.name,
            "icon": "https://i0.wp.com/yr-lang.com/wp-content/uploads/2019/12/YRLANGBLACK.png?fit=583%2C596&ssl=1"
        }
        send_user_notification(user=instance.user, payload=payload_data, ttl=100)
        send_mail(
            'Verification mail for ' + instance.requested_for.name + ' request',
            'Your Request has been verified for ' + instance.requested_for.name + '',
            development_example.EMAIL_HOST_USER,
            [str(instance.user.email)],
            fail_silently=True,
        )
        return redirect('client_request_detail', pk=instance.id)


class PublicProfile(DetailView):
    model = CustomUser
    template_name = 'users/public_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(PublicProfile, self).get_context_data(**kwargs)
        data_r = self.get_object()
        context['reviews'] = data_r.reviewee.all().order_by('date_posted')[:3]
        return context


class CreateRequestForLanguageVerifier(UserSessionAndLoginCheckMixing, UserPassesTestMixin, FormView):
    form_class = ClientToAdminRequestFormSet
    template_name = 'request_to_admin.html'

    def test_func(self):
        return self.request.user.is_client_user(self.request.session.get('user_role'))

    def get_context_data(self, **kwargs):
        context = super(CreateRequestForLanguageVerifier, self).get_context_data(**kwargs)
        context['banner'] = 'Request for Language Verifier'
        return context

    def form_valid(self, form):
        role = UserRole.objects.get(name=UserRole.LANGUAGE_VERIFIER)
        instance = UserRoleRequest.objects.create(user=self.request.user, requested_for=role)
        for frm in form:
            form_instance = frm.save(commit=False)
            form_instance.content_object = instance
            form_instance.save()
        messages.success(self.request, "Your Request For Become Language Verifier sent Successfully !")
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class BecomeProviderView(TemplateView):
    template_name = 'users/become_provider.html'

    # def test_func(self):
    #     return self.request.user.is_client_user(self.request.session.get('user_role'))


class BecomeLocaliteView(TemplateView):
    template_name = 'users/become_localite.html'

    # def test_func(self):
    #     return self.request.user.is_client_user(self.request.session.get('user_role'))


class AboutUsView(TemplateView):
    template_name = 'about_us.html'

class AddCityInUserFavoriteView(RedirectView):

    def get(self, request, *args, **kwargs):
        instance = CityPage.objects.get(id=kwargs.get('city_id'))
        if instance:
            UserFavorite.objects.create(content_object=instance, user=self.request.user)
        messages.success(self.request, "city addes in your favorite")
        return redirect('/')

class AddLocOrProInUserFavoriteView(RedirectView):

    def get(self, request, *args, **kwargs):
        instance = CustomUser.objects.get(id=kwargs.get('user_id'))
        if instance:
            UserFavorite.objects.create(content_object=instance, user=self.request.user)
        messages.success(self.request, "added in favorite !")
        return redirect('/')


class UserFavoriteListView(TemplateView):
    template_name = 'users/user_favorite_list.html'

    def get_context_data(self, **kwargs):
        self.provider_list = []
        self.localite_list = []
        context = super(UserFavoriteListView, self).get_context_data( **kwargs)
        content_type_city = ContentType.objects.get_for_model(CityPage)
        content_type_user = ContentType.objects.get_for_model(CustomUser)
        user_list = UserFavorite.objects.filter( content_type=content_type_user, user=self.request.user)
        city_list = UserFavorite.objects.filter(content_type=content_type_city, user=self.request.user)

        context['citys'] = [ i.content_object for i in city_list ]
        for user in user_list:
            if user.content_object.user_role.filter(name= UserRole.PROVIDER).exists():
                self.provider_list.append(user.content_object)
        for user in user_list:
            if user.content_object.user_role.filter(name=UserRole.LOCALITE).exists():
                self.localite_list.append(user.content_object)

        context['providers'] = self.provider_list
        context['localites'] = self.localite_list
        return context