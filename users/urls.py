from django.urls import path, re_path

from . import views

urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('account', views.AccountView.as_view(), name='account'),
    path('user-detail/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('provider-detail/<int:pk>', views.ProviderDetailView.as_view(), name='provider_detail'),
    path('user-role', views.UserMultipleRoleView.as_view(), name='user-role-select'),
    path("client_signup", views.ClientSignupView.as_view(), name='client_signup_view'),
    path("professional_signup", views.ProfessionalSignupView.as_view(), name='professional_account_signup'),
    path("request_for_provider", views.CreateRequestForProvider.as_view(), name='request_for_provider'),
    path("request_for_localite", views.CreateRequestForLocalite.as_view(), name='request_for_localite'),
    path("request_for_language_verifiers", views.CreateRequestForLanguageVerifier.as_view(),
         name='request_for_language_verifier'),
    path("request-detail/<int:pk>", views.AprovedClientRequestView.as_view(), name='client_request_detail'),
    path("request-list", views.UserRequestListView.as_view(), name='client_request_list'),
    path('public-profile/<int:pk>/', views.PublicProfile.as_view(), name='public_profile'),
    path("verify-client-request/<int:id>", views.VerifyClientRequestView.as_view(), name='verify_client_request'),
    path("become-provider", views.BecomeProviderView.as_view(), name='become_provider_temp'),
    path("become-localite", views.BecomeLocaliteView.as_view(), name='become_localite_temp'),
    path('about-us', views.AboutUsView.as_view(), name='about_us'),


    # favorites links for add
    path('favorites/<int:city_id>', views.AddCityInUserFavoriteView.as_view(), name='add_city_in_favorite'),
    path('favorites_/<int:user_id>', views.AddLocOrProInUserFavoriteView.as_view(), name='add_loc_or_pro_in_favorite'),
    path('user-favorites/', views.UserFavoriteListView.as_view(), name='user_favorite_list'),

]

import tellme
