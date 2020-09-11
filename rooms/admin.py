from django.contrib import admin
from .models import Room, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    can_delete = False


class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__', "date_created",'created_for')
    list_display_links = ('__str__',)
    list_filter = ('date_created', 'created_for')
    list_per_page = 25
    search_fields = ['creator__email', 'partner__email', 'date_created']
    inlines = [ MessageInline]


admin.site.register(Room, RoomAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', "date_created")
    list_display_links = ('__str__',)
    list_filter = ('date_created',)
    list_per_page = 25
    search_fields = ['creator__email', 'partner__email', 'date_created']


admin.site.register(Message, MessageAdmin)
