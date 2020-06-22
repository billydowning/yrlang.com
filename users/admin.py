from django.contrib import admin
from .models import (CustomUser, State, Language, Country, Profession,
                     UserRole, Categories, ProviderCategories, UserRoleRequest, UserVideos)
from invoices.models import Invoice
from appointments.models import Appointment
from blogpost.models.modelpost import BlogPostPage
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


class BlogPostInline(admin.TabularInline):
    model = BlogPostPage
    can_delete = False
    extra = 0
    classes = ['collapse', ]
    verbose_name_plural = 'Posts'


class RequestorInline(admin.TabularInline):
    model = Appointment
    fk_name = 'requestor'
    can_delete = False
    extra = 0
    classes = ['collapse', ]
    verbose_name_plural = 'Requestor'


class RequesteeInline(admin.TabularInline):
    model = Appointment
    fk_name = 'requestee'
    can_delete = False
    extra = 0
    classes = ['collapse', ]
    verbose_name_plural = 'Requestee'


class PayeeInline(admin.TabularInline):
    model = Invoice
    extra = 0
    can_delete = False
    fk_name = 'payee'
    classes = ['collapse', ]
    verbose_name_plural = 'Payee'


class PayorInline(admin.TabularInline):
    model = Invoice
    extra = 0
    can_delete = False
    fk_name = 'payor'
    classes = ['collapse', ]
    verbose_name_plural = 'Payor'


class ProviderCategoriesInline(admin.TabularInline):
    model = ProviderCategories
    fk_name = 'provider'
    can_delete = True
    extra = 0
    classes = ['collapse', ]
    verbose_name_plural = 'Provider Categories'


class CustomerAdmin(AuthUserAdmin):
    ordering = ('email',)
    list_display = ('__str__', 'is_client', 'phone_number')
    list_display_links = ('__str__',)
    list_filter = ('is_client', 'country', 'state')
    list_per_page = 25
    search_fields = ['email', 'language__name', 'country__name', 'state__name']
    fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', ('username', 'password'), 'is_client', 'is_private')
        }),
        ('Extra Info.', {
            'classes': ('collapse',),
            'fields': ('bio', 'phone_number', 'state',
                       'country', 'language', 'profession',
                       'stripe_id', 'user_role', 'profile_image'),
        }),
        ('Groups & Permission', {
            'classes': ('collapse',),
            'fields': ('groups',
                       'user_permissions',),
        }),
    )
    inlines = [RequestorInline, RequesteeInline,
               PayeeInline, PayorInline,
                ProviderCategoriesInline]


admin.site.register(CustomUser, CustomerAdmin)


class StateAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_display_links = ('__str__',)
    list_filter = ('name',)
    list_per_page = 25
    search_fields = ['name', ]


admin.site.register(State, StateAdmin)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_display_links = ('__str__',)
    list_filter = ('name',)
    list_per_page = 25
    search_fields = ['name', ]


admin.site.register(Language, LanguageAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_display_links = ('__str__',)
    list_filter = ('name',)
    list_per_page = 25
    search_fields = ['name', ]


admin.site.register(Country, CountryAdmin)


class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_display_links = ('__str__',)
    list_filter = ('name',)
    list_per_page = 25
    search_fields = ['name', ]


admin.site.register(Profession, ProfessionAdmin)


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_display_links = ('__str__',)
    list_filter = ('name',)
    search_fields = ['name', ]


admin.site.register(UserRole, UserRoleAdmin)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_display_links = ('__str__',)
    list_filter = ('name',)
    search_fields = ['name', ]
    fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('name',)
        }),
    )

admin.site.register(Categories, CategoriesAdmin)


admin.site.register(UserRoleRequest)
admin.site.register(UserVideos)