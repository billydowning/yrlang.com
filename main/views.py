from datetime import datetime
import pytz

from django.views.generic import TemplateView, View, ListView
from django.http import JsonResponse
from django.db.models import Q

from .constant import *
from users.models import CustomUser, UserRole, UserRoleRequest
from blogpost.models import BlogPostPage, CityPage
from appointments.models import Appointment, ProviderAppointment


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context["localites"] = CustomUser.objects.filter(is_client=False, is_private=False,
                                                         user_role__name__in=[UserRole.LOCALITE]). \
                                   exclude(id=self.request.user.id).exclude(state__isnull=True,
                                                                            country__isnull=True).order_by('?')[:3]
        context["providers"] = CustomUser.objects.filter(is_client=False, is_private=False,
                                                         user_role__name__in=[UserRole.PROVIDER]). \
                                   exclude(id=self.request.user.id).exclude(state__isnull=True,
                                                                            country__isnull=True).order_by('?')[:3]

        banner = ""
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                banner = "Logged in as Admin"
                context["requests"] = UserRoleRequest.objects.order_by('requested_on').filter(status=UserRoleRequest.REQUESTED,
                                                                    requested_for__name=UserRole.LANGUAGE_VERIFIER)
            elif self.request.user.is_client_user(self.request.session.get('user_role')):
                banner = "Logged in as Client"
            elif self.request.user.is_provider_user(self.request.session.get('user_role')):
                context['appointments'] = ProviderAppointment.objects.filter(requestee=self.request.user,
                                                                             status=ProviderAppointment.REQUESTED).order_by(
                    '-created_date')[:3]
                banner = "Logged in as Provider"
            elif self.request.user.is_localite_user(self.request.session.get('user_role')):
                context["bookings"] = Appointment.objects.filter(requestee=self.request.user).order_by('-date_created')[:3]
                banner = "Logged in as Localite"
            elif self.request.user.is_language_verifier_user(self.request.session.get('user_role')):
                context["requests"] = UserRoleRequest.objects.order_by('requested_on').filter(status=UserRoleRequest.REQUESTED,
                                                                      requested_for__name__in=[UserRole.LOCALITE, UserRole.PROVIDER]).exclude(user=self.request.user)[:3]
        elif self.request.user.is_anonymous:
            banner = "You Are not logged in "
        context["banner"] = banner
        return context


class Search(View):

    def get(self, request, *args, **kwargs2):
        q = request.GET.get('q', None)
        users = CustomUser.objects.filter(
            Q(username__startswith=q) |
            Q(username__startswith=q.capitalize()) |
            Q(first_name__startswith=q) |
            Q(first_name__startswith=q.capitalize()) |
            Q(last_name__startswith=q) |
            Q(email__startswith=q)
        ).filter(is_client=False, is_private=False).exclude(id=self.request.user.id)
        posts = BlogPostPage.objects.filter(title__icontains=q)
        cities = CityPage.objects.filter(title__icontains=q)

        users_lst = list(users.values('id', 'username', 'first_name', 'last_name', 'email'))
        posts_lst = list(posts.values('id', 'title'))
        cities_lst2 = [{'slug': '/' + city.get_parent().slug + '/' + city.slug, 'title': city.title} for city in cities]
        return JsonResponse({'professionals': users_lst, 'posts': posts_lst, 'cities': cities_lst2})


class TimeZone(View):

    def get(self, request, *args, **kwargs2):

        q = request.GET.get('q', None)

        user_timezone = datetime.now().astimezone(pytz.timezone(str(q))).replace(tzinfo=None)
        user_timezone2 = datetime.now().astimezone(pytz.timezone(str(q))).replace(minute=00, hour=SLOT_12, tzinfo=None)
        slots = {'s1': False, 's2': False}
        if user_timezone <= user_timezone2:
            slots = {'s1': False, 's2': False}
        else:
            user_timezone2 = datetime.now().astimezone(pytz.timezone(str(q))).replace(minute=00, hour=SLOT_06,
                                                                                      tzinfo=None)
            if user_timezone < user_timezone2:
                slots = {'s1': True, 's2': False}
            else:
                slots = {'s1': True, 's2': True}

        return JsonResponse({'slots': slots})


class ProviderListsView(ListView):
    template_name = "provider_list.html"
    context_object_name = 'providers'

    def get_queryset(self):
        state = self.kwargs.get('state_name', None)
        if state:
            query = CustomUser.objects.filter(is_client=False, is_private=False, state__name__icontains=state,
                                              user_role__name=UserRole.PROVIDER). \
                exclude(id=self.request.user.id).exclude(country__isnull=True).order_by('?')
        else:
            query = CustomUser.objects.filter(is_client=False, is_private=False,
                                              user_role__name=UserRole.PROVIDER). \
                exclude(id=self.request.user.id).exclude(state__isnull=True,
                                                         country__isnull=True).order_by('?')
        return query


class LocaliteListsView(ListView):
    template_name = "localite_list.html"
    context_object_name = 'localites'

    def get_queryset(self):
        state = self.kwargs.get('state_name', None)
        if state:
            query = CustomUser.objects.filter(is_client=False, is_private=False, state__name__icontains=state,
                                              user_role__name=UserRole.LOCALITE). \
                exclude(id=self.request.user.id).exclude(country__isnull=True).order_by('?')
        else:
            query = CustomUser.objects.filter(is_client=False, is_private=False,
                                              user_role__name=UserRole.LOCALITE). \
                exclude(id=self.request.user.id).exclude(state__isnull=True,
                                                         country__isnull=True).order_by('?')
        return query


class IndexView(TemplateView):
    template_name = 'explore.html'