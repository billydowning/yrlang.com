from django.urls import path

from main import views

app_name = 'main'
urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('location-ajax', views.SetLonAndLatInSession.as_view(), name='set_location_ajax'),
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.Search.as_view(), name='search'),
    path('time-zone/', views.TimeZone.as_view(), name='time_zone'),
    path('provider/', views.ProviderListsView.as_view(), name='provider_list'),
    path('provider/<str:state_name>', views.ProviderListsView.as_view(), name='provider_list'),
    path('localites/<str:state_name>', views.LocaliteListsView.as_view(), name='localite_list'),
    path('localites/', views.LocaliteListsView.as_view(), name='localite_list'),
    path('our-cities/<int:pk>/', views.OurCities.as_view(), name='our_cities'),
    path('our-cities/', views.OurCities.as_view(), name='our_cities'),

    # favorites URLS for anonymousUSER
    path('add-anon-favorite/<str:object>/<int:id>', views.AddAnonymousUserFavoriteView.as_view(),
         name='add_anon_favorite'),
    path('favorites/', views.ListOfnonymousUserFavoriteView.as_view(), name='anon_favorite_list'),

    path('blog-post/', views.BlogPostView.as_view(), name='blog-post'),

    path('join-team/', views.JoinOurTeam.as_view(), name='join_our_team'),
    path('faqs/', views.FAQS.as_view(), name='faqs'),
    path('terms-condition/', views.TermsCondition.as_view(), name='terms-condition'),
    path('trust-and-saftey/', views.TrustAndSaftey.as_view(), name='trust_and_saftey'),

]
