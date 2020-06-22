from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.models import Page, Orderable
from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from users.models import CustomUser, Country, UserRole
from django import forms


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

    def get_context(self, request, *args, **kwargs):
        city_id = self._get_pk_val()
        city = CityPage.objects.get(id=city_id)
        state=city.state
        context = super(CityPage, self).get_context(request, *args, **kwargs)
        context['localites'] = CustomUser.objects.filter(user_role__name=UserRole.LOCALITE,
                                                     is_private=False, state=state).\
            exclude(id=request.user.id).order_by('?')[:2]
        context['providers'] = CustomUser.objects.filter(user_role__name=UserRole.PROVIDER,
                                                     is_private=False,state=state).\
            exclude(id=request.user.id).order_by('?')[:2]
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
