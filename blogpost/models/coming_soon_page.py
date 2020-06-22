from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel


class ComingSoonPage(Page):
    description = models.CharField(blank=True, null=True, max_length=100,
                                   help_text='Describe About events.')
    body = RichTextField()
    date = models.DateField(null=True, blank=True,
                            help_text='Given the date for event')
    time = models.TimeField(null=True, blank=True, help_text='Give the time for event')

    def first_image(self):
        gallery_image = self.gallery_images.first()
        if gallery_image:
            return gallery_image.image
        else:
            return None

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('time'),
        ], heading='Time and Date For the event'),
        FieldPanel('body'),
        InlinePanel("gallery_images", label='Gallery Images'),

    ]
    parent_page_types = ['ComingSoonIndexPage']


class ComingSoonIndexPage(Page):
    introduction = models.CharField(blank=True, null=True, max_length=100,
                                    help_text='Introduction about new events.')

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        comingsoon = self.get_children().live().order_by('-first_published_at')
        context['comingsoon'] = comingsoon
        return context

    subpage_types = ['ComingSoonPage']


class ComingSoonPageGalleryImages(Orderable):
    page = ParentalKey(ComingSoonPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.CASCADE,
                              related_name='+',
                              help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
                              )

    panels = [
        ImageChooserPanel("image")
    ]
