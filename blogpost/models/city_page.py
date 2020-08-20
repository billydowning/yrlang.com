from django import forms
from django.db import models
from django.urls import reverse

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from users.models import CustomUser, UserRole, State
# from users.models import( UserRole, CustomUser)
from .brucke_page import (BruckePage)
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point


class CityPage(Page):
    introduction = models.TextField(blank=True,
                                    help_text='Text to Describe the page')
    things_to_do = RichTextField(blank=True,
                                 help_text='describe the thing that we are allow to do ')
    language = ParentalManyToManyField('users.Language', blank=True)
    currency = models.CharField(blank=True, null=True, max_length=100,
                                help_text='Describe about Currency and Credit Cards')
    state = models.ForeignKey("users.State", blank=True,
                              null=True, on_delete=models.SET_NULL,
                              related_name='+',
                              help_text='select the city name instate of state '
                              )

    def main_image(self):
        gallery_item = self.gallery_image.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('state'),
        InlinePanel("gallery_image", label='Gallery Images'),
        FieldPanel('things_to_do'),
        FieldPanel('currency'),
        MultiFieldPanel([
            FieldPanel(
                'language',
                widget=forms.CheckboxSelectMultiple,
            ),
        ],
            heading='Select languange that are Spoken in City '

        )

    ]

    def get_absolute_url(self):
        return reverse('main:our_cities', args=[self.pk])

    def get_context(self, request, *args, **kwargs):
        context = super(CityPage, self).get_context(request, *args, **kwargs)
        if request.session.get('log') and request.session.get('lat'):
            self.latitude = request.session.get('lat')
            self.longitude = request.session.get('log')
            user_location = Point(float(self.longitude), float(self.latitude), srid=4326)
            state_data = State.objects.filter(name=str(self.state)).annotate(distance=Distance('location', user_location)).order_by('distance').first()
            context['distance'] = 'You are ' +str(state_data.distance)[:10] + ' meter away'

            localites_list = state_data.customuser_set.filter(is_private=False,
                                                          user_role__name__in=[UserRole.LOCALITE]
                                                                 ).exclude(id=request.user.id).order_by('?')
            provider_list = state_data.customuser_set.filter(is_private=False,
                                                          user_role__name__in=[UserRole.PROVIDER]
                                                          ).exclude(id=request.user.id).order_by('?')
        else:
            localites_list =  CustomUser.objects.filter(user_role__name=UserRole.LOCALITE,
                                                     is_private=False, state__name=self.state).\
            exclude(id=request.user.id).order_by('?')
            provider_list =  CustomUser.objects.filter(user_role__name=UserRole.PROVIDER,
                                                     is_private=False, state__name=self.state).\
            exclude(id=request.user.id).order_by('?')
        context['localite_total'] = str(localites_list.count()) + ' localites in city'
        context['localites'] = localites_list[:2]
        context['providers'] = provider_list[:2]
        context['brukes'] = BruckePage.objects.filter(state=self.state)[:3]
        return context

    parent_page_types = ['CityIndexPage']


class CityIndexPage(Page):
    introduction = models.CharField(blank=True, null=True, max_length=100,
                                    help_text='Introduction about city (into 100 Character) ')
    image = models.ForeignKey('wagtailimages.Image',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              related_name='+',
                              help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
                              )

    def get_context(self, request):
        context = super().get_context(request)
        citypages = self.get_children().live().order_by('-first_published_at')
        context['citys'] = citypages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        ImageChooserPanel('image'),
    ]

    subpage_types = ['CityPage']


class CityPageGalleryImages(Orderable):
    page = ParentalKey(CityPage, on_delete=models.CASCADE, related_name='gallery_image')
    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.CASCADE,
                              related_name='+',
                              help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
                              )

    panels = [
        ImageChooserPanel("image")
    ]
