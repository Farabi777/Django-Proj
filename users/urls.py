from django.urls import path
from . import views
from .views import profile_view, edit_profile

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('profile/', profile_view, name='profile'),

]
