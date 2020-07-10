from django.urls import path

from main import views

app_name = 'main'
urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.Search.as_view(), name='search'),
    path('time-zone/', views.TimeZone.as_view(), name='time_zone'),
    path('provider/', views.ProviderListsView.as_view(), name='provider_list'),
    path('provider/<str:state_name>', views.ProviderListsView.as_view(), name='provider_list'),
    path('localites/<str:state_name>', views.LocaliteListsView.as_view(), name='localite_list'),
    path('localites/', views.LocaliteListsView.as_view(), name='localite_list'),
    path('our-cities/<int:pk>/', views.OurCities.as_view(), name='our_cities'),
    path('our-cities/', views.OurCities.as_view(), name='our_cities'),
]
