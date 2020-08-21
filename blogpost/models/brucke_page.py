from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel


class BruckePage(Page):
    date = models.DateField(auto_now=True)
    bruke_content = RichTextField(blank=True,
                                  help_text='describe the thing that we are allow to do ')
    image = models.ForeignKey('wagtailimages.Image',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              related_name='+',
                              help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
                              )
    state = models.ForeignKey("users.State", blank=True,
                              null=True, on_delete=models.SET_NULL,
                              related_name='+',
                              help_text='select the city name instate of state '
                              )

    content_panels = Page.content_panels + [
        FieldPanel('state'),
        FieldPanel('bruke_content'),
        ImageChooserPanel('image'),
        InlinePanel('related_posts', label="Related Post"),

    ]
    parent_page_types = ['BruckeIndexPage']

    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context['state_brucks'] = BruckePage.objects.filter(state=self.state).exclude(id=self.pk)
        return context


class BruckeIndexPage(Page):
    introduction = models.CharField(blank=True, null=True, max_length=100,
                                    help_text='Introduction about Bruckes .')
    image = models.ForeignKey('wagtailimages.Image',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              related_name='+',
                              help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
                              )

    def get_context(self, request):
        context = super().get_context(request)
        bruckepages = self.get_children().live().order_by('-first_published_at')
        context['bruckepage'] = bruckepages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        ImageChooserPanel('image'),
    ]

    subpage_types = ['BruckePage']


class BruckeRelatedPosts(Orderable):
    page = ParentalKey(BruckePage, on_delete=models.CASCADE, related_name='related_posts')
    title = models.CharField('title', null=True, blank=True,
                             max_length=30)
    image = models.ForeignKey('wagtailimages.Image',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              related_name='+',
                              help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
                              )
    body = RichTextField(" Descriptions ")
    check_out = models.TextField(null=True, blank=True,
                                 help_text="What you like to visit here "
                                 )
    walking_distance = models.CharField('Distance', null=True, blank=True,
                                        max_length=20,
                                        help_text="Distance from main City Point."
                                        )

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('body'),
        FieldPanel('check_out'),
        FieldPanel('walking_distance'),

    ]
