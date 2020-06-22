from django.contrib import admin
from .models import Review, Notification


# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('__str__', "user")
    list_display_links = ('__str__',)
    list_filter = ('name', 'user',)
    list_per_page = 25
    search_fields = ['user', 'name', ]


admin.site.register(Notification, NotificationAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__', "date_posted")
    list_display_links = ('__str__',)
    list_filter = ('date_posted',)
    list_per_page = 25
    search_fields = ['user', 'name', ]


admin.site.register(Review, ReviewAdmin)
