from django.urls import path
from . import views
from .views import register_view, login_view, logout_view
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet



urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('add/', views.add_movie, name='add_movie'),
    path('edit/<int:pk>/', views.edit_movie, name='edit_movie'),
    path('delete/<int:pk>/', views.delete_movie, name='delete_movie'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('search/', views.movie_search, name='movie_search'),
    path('friends/', views.friend_list, name='friend_list'),
    path('friends/add/<int:user_id>/', views.add_friend, name='add_friend'),
    path('friends/remove/<int:user_id>/', views.remove_friend, name='remove_friend'),
]
