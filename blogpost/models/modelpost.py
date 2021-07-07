from django.db import models
from users.models import CustomUser
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel


class BlogPostPage(Page):
    date_posted = models.DateField(auto_now=True)
    content = RichTextField(blank=True,
                            help_text='describe your blog our here ! ')


    content_panels = Page.content_panels + [

        FieldPanel('content'),


    ]

    parent_page_types = ['BlogPostIndexPage']

    def __str__(self):
        return self.title


class BlogPostIndexPage(Page):
    name = models.CharField(blank=True, null=True, max_length=100,
                            help_text='categories your blog . ')

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blog'] = blogpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('name'),

    ]
    subpage_types = ['BlogPostPage']
