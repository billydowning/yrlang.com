from django.shortcuts import resolve_url, redirect
from django.conf import settings
from blogpost.models.city_page import CityPage
from django.contrib.contenttypes.models import ContentType
from users.models import UserRole, CustomUser, UserFavorite
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter as DefaultSocialAdepter


# custom adapter for user redirect user is client or not
class MyAccountAdapter(DefaultAccountAdapter):

    def logout(self, request):
        if request.session.get('user_role'):
            del request.session['user_role']
        return super(MyAccountAdapter, self).logout(request)

    def get_login_redirect_url(self, request):

        if request.user.user_role.count() > 1:
            return resolve_url("/users/user-role")
        if self.request.user.user_role.filter(name=UserRole.CLIENT).exists():
            self.request.session['user_role'] = UserRole.CLIENT
            return resolve_url(settings.LOGIN_REDIRECT_URL)
        elif self.request.user.user_role.filter(name=UserRole.PROVIDER).exists():
            if request.user.phone_number is None \
                    and request.user.country is None \
                    and request.user.state is None:
                self.request.session['user_role'] = UserRole.PROVIDER
                url = '/users/profile'
                return resolve_url(url)
            else:
                self.request.session['user_role'] = UserRole.PROVIDER
                return resolve_url(settings.LOGIN_REDIRECT_URL)
        elif self.request.user.user_role.filter(name=UserRole.LOCALITE).exists():
            if request.user.phone_number is None \
                    and request.user.country is None \
                    and request.user.state is None:
                self.request.session['user_role'] = UserRole.LOCALITE
                url = '/users/profile'
                return resolve_url(url)
            else:
                self.request.session['user_role'] = UserRole.LOCALITE
                return resolve_url(settings.LOGIN_REDIRECT_URL)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)


class MySocialAccountAdepter(DefaultSocialAdepter):
    def get_connect_redirect_url(self, request, socialaccount):
        if not socialaccount.account.user.user_role.exists():
            role = UserRole.objects.get(name=UserRole.CLIENT)
            socialaccount.account.user.user_role.add(role)
            return resolve_url('/')
        return resolve_url('/')

    def save_user(self, request, sociallogin, form=None):
        user = super(MySocialAccountAdepter, self).save_user(request, sociallogin, form=None)
        if not user.user_role.exists():
            role = UserRole.objects.get(name=UserRole.CLIENT)
            user.user_role.add(role)
        return user
