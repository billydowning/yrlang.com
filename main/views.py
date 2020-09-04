from datetime import datetime
import pytz
from django.contrib import messages
from _collections import defaultdict
from django.views.generic import (TemplateView, View, ListView,
                                  DetailView, RedirectView, CreateView)

from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from .constant import *
from users.models import CustomUser, UserRole, UserRoleRequest, State
from blogpost.models import BlogPostPage, CityPage, BruckePage
from appointments.models import Appointment, ProviderAppointment
from .forms import UserSearchFrom, BookingReviewForm
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.http import HttpResponseRedirect, JsonResponse
from .models import Review
from appointments.models import (Appointment as BookingModel,
                                 ProviderAppointment as AppointmentModel)

class HomeView(TemplateView):
    template_name = "home.html"


    def get(self, request, *args, **kwargs):
        localite_list = None
        provider_list = None
        search_form = UserSearchFrom(self.request.GET)



        if search_form.is_valid():
            if search_form.cleaned_data.get('country'):
                localite_list = CustomUser.objects.filter(Q(country=search_form.cleaned_data.get('country'))). \
                                    filter(is_private=False, user_role__name__in=[UserRole.LOCALITE]). \
                                    exclude(id=self.request.user.id, state__isnull=True, country__isnull=True).order_by(
                    '?')[:3]
                provider_list = CustomUser.objects.filter(Q(country=search_form.cleaned_data.get('country'))). \
                                    filter(is_private=False, user_role__name__in=[UserRole.PROVIDER]). \
                                    exclude(id=self.request.user.id, state__isnull=True, country__isnull=True).order_by(
                    '?')[:3]

            elif request.user.is_authenticated and request.user.last_location:
                provider_list = CustomUser.objects.filter(is_private=False,
                                                          user_role__name__in=[UserRole.PROVIDER]). \
                                    exclude(id=self.request.user.id).exclude(state__isnull=True,
                                                                             country__isnull=True).\
                                    annotate(distance=Distance('last_location',request.user.last_location)).order_by('distance')[:3]
                localite_list = CustomUser.objects.filter(is_private=False,
                                                          user_role__name__in=[UserRole.LOCALITE]). \
                                    exclude(id=self.request.user.id).exclude(state__isnull=True,
                                                                             country__isnull=True).\
                                    annotate(distance=Distance('last_location',request.user.last_location)).order_by('distance')[:3]


            else:
                localite_list = CustomUser.objects.filter(is_private=False,
                                                          user_role__name__in=[UserRole.LOCALITE]). \
                                    exclude(id=self.request.user.id).exclude(state__isnull=True,
                                                                             country__isnull=True).order_by('?')[:3]
                provider_list = CustomUser.objects.filter(is_private=False,
                                                          user_role__name__in=[UserRole.PROVIDER]). \
                                    exclude(id=self.request.user.id).exclude(state__isnull=True,
                                                                             country__isnull=True).order_by('?')[:3]




        context = self.get_context_data(**kwargs)
        context["localites"] = localite_list
        context['providers'] = provider_list
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        search_form = UserSearchFrom(self.request.GET)
        banner = ""
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                banner = "Logged in as Admin"
                context["requests"] = UserRoleRequest.objects.order_by('requested_on').filter(
                    status__in=[UserRoleRequest.REQUESTED, UserRoleRequest.VERIFIED],
                    requested_for__name=UserRole.LANGUAGE_VERIFIER).exclude(user=self.request.user)[:3]
            elif self.request.user.is_client_user(self.request.session.get('user_role')):
                banner = "Logged in as Client"
            elif self.request.user.is_provider_user(self.request.session.get('user_role')):
                context['appointments'] = ProviderAppointment.objects.filter(requestee=self.request.user,
                                                                             status=ProviderAppointment.REQUESTED).order_by(
                    '-created_date')[:3]
                banner = "Logged in as Provider"
            elif self.request.user.is_localite_user(self.request.session.get('user_role')):
                context["bookings"] = Appointment.objects.filter(requestee=self.request.user).order_by('-date_created')[
                                      :3]
                banner = "Logged in as Localite"
            elif self.request.user.is_language_verifier_user(self.request.session.get('user_role')):
                context["requests"] = UserRoleRequest.objects.order_by('requested_on').filter(
                    status__in=[UserRoleRequest.REQUESTED, UserRoleRequest.VERIFIED],
                    requested_for__name__in=[UserRole.PROVIDER, UserRole.LOCALITE]).exclude(user=self.request.user)[:3]
        elif self.request.user.is_anonymous:
            banner = "You Are not logged in "
        context["banner"] = banner

        context['search_form'] = search_form
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


class BlogPostView(TemplateView):
    template_name = 'blogpost/brucke_page_home.html'

    def get_context_data(self, **kwargs):
        context = super(BlogPostView, self).get_context_data()
        context['brucks'] = BruckePage.objects.all().order_by("date")
        return context


class OurCities(DetailView):
    model = CityPage
    template_name = 'our-cities.html'
    context_object_name = 'city'

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if not pk:
            self.kwargs['pk'] = self.model.objects.first()
        return super(OurCities, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OurCities, self).get_context_data()
        context['cities'] = self.get_queryset()
        obj = self.get_object()
        if obj.state:
            providers = CustomUser.objects.filter(
                is_client=False, is_private=False,
                state__name__icontains=obj.state,
                user_role__name=UserRole.PROVIDER
            ).exclude(id=self.request.user.id).exclude(country__isnull=True).order_by('?')

            localites = CustomUser.objects.filter(
                is_client=False, is_private=False,
                state__name__icontains=obj.state,
                user_role__name=UserRole.LOCALITE
            ).exclude(id=self.request.user.id).exclude(country__isnull=True).order_by('?')
        else:
            providers = CustomUser.objects.filter(
                is_client=False, is_private=False,
                user_role__name=UserRole.PROVIDER
            ).exclude(id=self.request.user.id) \
                .exclude(state__isnull=True, country__isnull=True).order_by('?')

            localites = CustomUser.objects.filter(
                is_client=False, is_private=False,
                user_role__name=UserRole.LOCALITE
            ).exclude(id=self.request.user.id) \
                .exclude(state__isnull=True, country__isnull=True).order_by('?')

        context['providers'] = providers
        context['localites'] = localites
        return context


class AddAnonymousUserFavoriteView(RedirectView):

    def get(self, request, *args, **kwargs):
        key = kwargs.get('object')
        fav_dic = request.session.get('favorites_dic') or dict()
        if key in fav_dic:
            if kwargs.get('id') not in fav_dic[kwargs.get('object')]:
                fav_dic[kwargs.get('object')].append(kwargs.get('id'))
            else:
                messages.success(request, "Already in Favorite")
                return redirect('/')
        else:
            fav_dic[kwargs.get('object')] = [kwargs.get('id')]
        request.session['favorites_dic'] = fav_dic
        messages.success(request, "Added in Favorite")
        return redirect('/')


class ListOfnonymousUserFavoriteView(TemplateView):
    template_name = 'users/anonymoususer_favorite_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListOfnonymousUserFavoriteView, self).get_context_data(**kwargs)
        self.localite = 'localite'
        self.provider = 'provider'
        self.city = 'city'
        if self.request.session.get('favorites_dic'):
            if self.localite in self.request.session.get('favorites_dic'):
                context['localites'] = CustomUser.objects.filter(is_private=False,
                                                                 id__in=self.request.session['favorites_dic'][
                                                                     'localite']). \
                    exclude(id=self.request.user.id).exclude(state__isnull=True,
                                                             country__isnull=True).order_by('?')
            if self.provider in self.request.session.get('favorites_dic'):
                context['providers'] = CustomUser.objects.filter(is_private=False,
                                                                 id__in=self.request.session['favorites_dic'][
                                                                     'provider']). \
                    exclude(id=self.request.user.id).exclude(state__isnull=True,
                                                             country__isnull=True).order_by('?')
            if self.city in self.request.session.get('favorites_dic'):
                context['citys'] = CityPage.objects.filter(id__in=self.request.session['favorites_dic']['city'])
        return context


class JoinOurTeam(TemplateView):
    template_name = 'main_join_our_team.html'


class TermsCondition(TemplateView):
    template_name = 'term_condition.html'


class TrustAndSaftey(TemplateView):
    template_name = 'main_trust_and_saftey.html'

class FAQS(TemplateView):
    template_name = 'FAQ.html'


class SetLonAndLatInSession(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.user.is_authenticated:
                last_loc = Point(float(request.GET.get('longitude')), float(request.GET.get('latitude')),srid=4326)
                cur_user = CustomUser.get(request.user.id)
                cur_user.last_location = last_loc
                cur_user.save()
                return JsonResponse(data={'already_here': 'data set'})
            elif not request.session.get('log') and not request.session.get('lat'):
                request.session['log']  = request.GET.get('longitude')
                request.session['lat'] = request.GET.get('latitude')
                return JsonResponse(data={'not_here': 'data set'})
            else:
                return JsonResponse(data={'already_here':'data found'})
        return True


class BookingRatingAndReview(CreateView):
    template_name = 'booking_rating_and_review.html'
    model = Review
    form_class = BookingReviewForm


    def form_valid(self, form):
        booking_obj = self.get_object()
        if self.request.user == booking_obj.requestor:
            partner = booking_obj.requestee
        else:
            partner = booking_obj.requestor
        review_form = form.save(commit=False)
        review_form.reviewer = self.request.user
        review_form.reviewee = partner
        review_form.content_object= booking_obj
        review_form.save()
        messages.success(self.request, "Review submited")
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        obj = get_object_or_404(BookingModel, pk=self.kwargs.get('bookoing_id'))
        return obj

    def get_context_data(self, **kwargs):
        context = super(BookingRatingAndReview, self).get_context_data(**kwargs)
        booking_obj = self.get_object()
        context['booking'] = booking_obj
        if self.request.user == booking_obj.requestor:
            partner = booking_obj.requestee
        else:
            partner = booking_obj.requestor
        context['partner'] = partner
        return context


class AppointmentRatingAndReview(CreateView):
    template_name = 'appointment_rating_and_review.html'
    model = Review
    form_class = BookingReviewForm


    def form_valid(self, form):
        booking_obj = self.get_object()
        if self.request.user == booking_obj.requestor:
            partner = booking_obj.requestee
        else:
            partner = booking_obj.requestor
        review_form = form.save(commit=False)
        review_form.reviewer = self.request.user
        review_form.reviewee = partner
        review_form.content_object= booking_obj
        review_form.save()
        messages.success(self.request, "Review submited")
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        obj = get_object_or_404(AppointmentModel, pk=self.kwargs.get('appointment_id'))
        return obj

    def get_context_data(self, **kwargs):
        context = super(AppointmentRatingAndReview, self).get_context_data(**kwargs)
        booking_obj = self.get_object()
        context['booking'] = booking_obj
        if self.request.user == booking_obj.requestor:
            partner = booking_obj.requestee
        else:
            partner = booking_obj.requestor
        context['partner'] = partner
        return context
