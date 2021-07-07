from django.urls import path

from . import views

urlpatterns = [
    path('new-post', views.PostCreateView.as_view(), name="new_post"),
    path('post/<int:post_id>', views.PostView.as_view(), name="post"),
    path('post/delete/<int:pk>', views.PostDelete.as_view(), name="delete_post"),
    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name="update_post"),
]