from allauth.account.adapter import get_adapter
from allauth.account.forms import SignupForm
from allauth.account.utils import setup_user_email
from django import forms
from django.forms import ModelForm
from multiupload.fields import MultiMediaField
from .models import (CustomUser, UserRole, Categories, ProviderCategories, UserVideos, UserRoleRequest)
from .utils import group_obj
from django.forms import modelformset_factory, BaseModelFormSet
from django.core.mail import send_mail
from yrlang.settings.development_example import EMAIL_HOST_USER
from rooms.models import Room, Message

class ClientSignupForm(SignupForm):
    terms = forms.BooleanField(widget=forms.CheckboxInput())

    def clean_terms(self):
        terms = self.cleaned_data['terms']
        if not terms:
            raise forms.ValidationError("You have not accept Terms and Conditions")
        return terms

    def save(self, request):
        user = super(ClientSignupForm, self).save(request)
        role = UserRole.objects.get(name=UserRole.CLIENT)
        chat_role = UserRole.objects.get(name=UserRole.ADMIN)
        user.user_role.add(role)
        admin = CustomUser.objects.filter(is_staff=True).order_by('date_joined').first()
        room_id = Room.create(admin, user, chat_role)
        Message.objects.create(author=admin, reciepent=user, content='Hello User', room=room_id)
        send_mail(
            'Welcome To YR-lang ' ,
            'Your account fo the YR-lang is been created welcome to our family of YR-lang.',
            EMAIL_HOST_USER,
            [str(user.email)],
            fail_silently=True,
        )
        return user


# Professional Signup Form override with allauth SignupForm
class ProfessionalSignupForm(SignupForm):
    role = forms.ModelChoiceField(
        queryset=UserRole.objects.exclude(name=UserRole.CLIENT),
        required=True
    )

    terms = forms.BooleanField(widget=forms.CheckboxInput())

    def clean_terms(self):
        terms = self.cleaned_data['terms']
        if not terms:
            raise forms.ValidationError("You have not accept Terms and Conditions")
        return terms

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        role = self.cleaned_data['role']
        user.is_client = False
        group_obj(user=user)
        user.save()
        if str(role) == UserRole.LOCALITE:
            user_role = UserRole.objects.get(name=UserRole.LOCALITE)
            user.user_role.add(user_role)
        else:
            user_role = UserRole.objects.get(name=UserRole.PROVIDER)
            user.user_role.add(user_role)
        return user


# Localite profile
class ProfessionalAccountForm(ModelForm):
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        )
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProfessionalAccountForm, self).__init__(*args, **kwargs)
        self.fields['state'].required = True
        self.fields['country'].required = True
        self.fields['phone_number'].required = True
        self.fields['phone_number'].widget.attrs.update({
            'autocomplete': 'off', 'type': 'tel',
            'pattern': "[0-9]{3}-[0-9]{3}-[0-9]{4}",

        })

    class Meta:
        model = CustomUser
        fields = ['bio', 'phone_number', 'state', 'country', 'language',
                  'profession', 'profile_image', 'is_private', 'multi_day']
        help_texts = {
            'phone_number': 'Use Formate Like This 999-999-9999 ',
            'multi_day': 'Allow Customer Multi-Day Booking '
        }

    def save(self, commit=True):
        instance = super(ProfessionalAccountForm, self).save()
        profile_image = self.request.FILES.get('profile_image', None)
        if profile_image:
            instance.profile_image = profile_image
            instance.save()
        return instance


# Localite account
class UpdateProfessionalAccountForm(ModelForm):
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        )
    )
    role = forms.ModelChoiceField(
        queryset=UserRole.objects.exclude(name=UserRole.LOCALITE),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'phone_number', 'state',
                  'country', 'language', 'profession', 'profile_image', 'is_private', 'multi_day']
        help_texts = {
            'phone_number': 'Use Formate Like This +91999-999-9999 ',
            'multi_day': 'Allow Customer Multi-Day Booking '
        }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(UpdateProfessionalAccountForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = UserRole.objects.exclude(id__in=self.instance.user_role.all())
        self.fields['phone_number'].widget.attrs.update({
            'autocomplete': 'off', 'type': 'tel',
            'pattern': "[\+]\d{2}\d{3}[\-]\d{3}[\-]\d{4}",

        })

    def save(self, commit=True):
        instance = super(UpdateProfessionalAccountForm, self).save(commit=False)
        role = self.cleaned_data['role']
        profile_image = self.request.FILES.get('profile_image', None)

        if role:
            if str(role) == UserRole.PROVIDER:
                user_role = UserRole.objects.get(name=UserRole.PROVIDER)
                instance.user_role.add(user_role)
                self.request.session['role_flag'] = UserRole.PROVIDER
            elif str(role) == UserRole.CLIENT:
                user_role = UserRole.objects.get(name=UserRole.CLIENT)
                instance.user_role.add(user_role)

        if profile_image:
            instance.profile_image = profile_image
        instance.save()
        return instance


# client account
class UpdateAccountForm(ModelForm):
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        )
    )
    role = forms.ModelChoiceField(
        queryset=UserRole.objects.exclude(name=UserRole.PROVIDER),
        required=False
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(UpdateAccountForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = UserRole.objects.exclude(id__in=self.instance.user_role.all())
        self.fields['phone_number'].required = True
        self.fields['phone_number'].widget.attrs.update({
            'autocomplete': 'off', 'type': 'tel',
            'pattern': "[\+]\d{2}\d{3}[\-]\d{3}[\-]\d{4}",

        })

    class Meta:
        model = CustomUser
        fields = ["username", "email", 'profile_image', 'phone_number']
        help_texts = {
            'phone_number': 'Use Formate Like This +91999-999-9999 '
        }

    def save(self, commit=True):
        instance = super(UpdateAccountForm, self).save(commit=False)
        role = self.cleaned_data['role']
        profile_image = self.request.FILES.get('profile_image', None)

        if role:
            if str(role) == UserRole.PROVIDER:
                user_role = UserRole.objects.get(name=UserRole.PROVIDER)
                instance.user_role.add(user_role)
                self.request.session['role_flag'] = UserRole.PROVIDER
            elif str(role) == UserRole.LOCALITE:
                user_role = UserRole.objects.get(name=UserRole.LOCALITE)
                instance.user_role.add(user_role)
                self.request.session['role_flag'] = UserRole.LOCALITE

        if profile_image:
            instance.profile_image = profile_image
        instance.save()
        return instance


class UserChoiceForm(ModelForm):
    class Meta:
        model = UserRole
        fields = ['name']
        widgets = {
            'name': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(UserChoiceForm, self).__init__(*args, **kwargs)
        self.fields['name'].choices = self.fields['name'].choices[1:]


# provider profile
class ProviderAccountForm(ModelForm):
    categories = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ['country', 'state', 'phone_number']
        help_texts = {
            'phone_number': 'Use Formate Like This +91999-999-9999 '
        }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProviderAccountForm, self).__init__(*args, **kwargs)
        self.fields['state'].required = True
        self.fields['country'].required = True
        self.fields['phone_number'].required = True
        self.fields['phone_number'].widget.attrs.update({
            'autocomplete': 'off', 'type': 'tel',
             'pattern': "[\+]\d{2}\d{3}[\-]\d{3}[\-]\d{4}",

        })

    def save(self, commit=True):
        instance = super(ProviderAccountForm, self).save()
        categories = self.cleaned_data['categories']
        if not instance.providercategories_set.filter(category=categories).exists():
            ProviderCategories.objects.create(
                category=categories,
                provider=instance
            )
        return instance


# provider account
class UpdateProviderAccountForm(ModelForm):
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        )
    )
    role = forms.ModelChoiceField(
        queryset=UserRole.objects.exclude(name=UserRole.PROVIDER),
        required=False
    )
    categories = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'phone_number', 'state',
                  'country', 'language', 'profile_image']
        help_texts = {
            'phone_number': 'Use Formate Like This +91999-999-9999 '
        }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(UpdateProviderAccountForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = UserRole.objects.exclude(id__in=self.instance.user_role.all())
        self.fields['phone_number'].widget.attrs.update({
            'autocomplete': 'off', 'type': 'tel',
            'pattern': "[\+]\d{2}\d{3}[\-]\d{3}[\-]\d{4}",
        })

    def save(self, commit=True):
        instance = super(UpdateProviderAccountForm, self).save()
        role = self.cleaned_data['role']
        categories = self.cleaned_data['categories']
        profile_image = self.request.FILES.get('profile_image', None)

        if role:
            if str(role) == UserRole.LOCALITE:
                user_role = UserRole.objects.get(name=UserRole.LOCALITE)
                instance.user_role.add(user_role)
                self.request.session['role_flag'] = UserRole.LOCALITE
            elif str(role) == UserRole.CLIENT:
                user_role = UserRole.objects.get(name=UserRole.CLIENT)
                instance.user_role.add(user_role)

        if categories:
            if not instance.providercategories_set.filter(category=categories).exists():
                ProviderCategories.objects.create(
                    category=categories,
                    provider=instance
                )

        if profile_image:
            instance.profile_image = profile_image
        instance.save()
        return instance


class ClientToAdminRequestForm(forms.ModelForm):

    class Meta:
        model = UserVideos
        fields = ['language', 'files']


class BaseAdminRequestFormset(BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        super(BaseAdminRequestFormset, self).__init__(*args, **kwargs)
        self.queryset= UserVideos.objects.none()

    def clean(self):
        super(BaseAdminRequestFormset, self).clean()
        lst = []
        for form in self.forms:
            if not form.is_valid():
                return
            if self.can_delete and self._should_delete_form(form):
                continue
            lang = form.cleaned_data.get('language')
            file = form.cleaned_data.get('files')
            if file is None:
                form.add_error('files', "Please Provide File!")
            if lang  in lst or lang is None:
                form.add_error('language', "Please Chose Proper Language !")
            else:
                lst.append(lang)



ClientToAdminRequestFormSet = modelformset_factory(UserVideos, formset=BaseAdminRequestFormset,
                                                   form=ClientToAdminRequestForm, min_num=1, extra=0,
                                                   max_num=4
                                                   )

from datetime import date


class RequestVerificationForm(forms.ModelForm):
    class Meta:
        model = UserRoleRequest
        fields = ['reason', 'meeting_on']

    def __init__(self, *args, **kwargs):
        self.model_object = kwargs.pop('model_object', None)
        super(RequestVerificationForm, self).__init__(*args, **kwargs)
        self.fields['meeting_on'].input_formats = ['%Y.%m.%d %H:%M']
        if self.model_object.meeting_on:
            today = date.today()
            difference = today - self.model_object.meeting_on.date()
            if difference.days == -1 or  difference.days == 0:
                self.fields.pop('meeting_on')

class RequestForCallForm(forms.Form):
    to = forms.EmailField(widget=forms.HiddenInput(), required=True)
    reason = forms.CharField(required=True, widget=forms.Textarea())
    req_from = forms.EmailField(required=True, label='email')
