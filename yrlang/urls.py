"""yrlang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
# wagtail
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [   re_path(r'^tellme/', include("tellme.urls")),
                  re_path(r'^webpush/', include('webpush.urls')),
                  path('paypal/', include('paypal.standard.ipn.urls')),
                  path('admin/', admin.site.urls),
                  path('accounts/', include('allauth.urls')),
                  path('', include('main.urls')),
                  path('users/', include('users.urls')),
                  path('user-admin/', include('custom_admin.urls')),
                  path('rooms/', include('rooms.urls')),
                  path('', include('appointments.urls')),
                  path('', include('blogpost.urls')),
                  path('', include('invoices.urls')),
                  path('payment/', include('payment.urls')),
                  re_path(r'^ratings/', include('star_ratings.urls', namespace='ratings' )),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# wagtail Url
urlpatterns += [
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    path('', include(wagtail_urls)),
]



if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns



#admin site Configurations
admin.site.site_header = 'Yr-lang'
admin.site.site_title = 'Yr-lang admin'
admin.site.index_title = 'Yr-lang administration'
