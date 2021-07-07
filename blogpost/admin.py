from django.contrib import admin
from blogpost.models.modelpost import BlogPostPage

# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_posted',  )
    list_display_links = ('__str__', )
    list_filter = ('date_posted',  )
    list_per_page = 25
    search_fields = ['date_posted', 'title']


admin.site.register(BlogPostPage, )
