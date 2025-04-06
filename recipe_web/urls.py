from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipes/",login_required(views.recipe_list), name="recipe_list"),
    path("recipe/create/", views.recipe_create, name="recipe_create"),
    path("recipe/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("recipe/<int:pk>/edit/", views.recipe_edit, name="recipe_edit"),
    path("recipe/<int:pk>/delete/", views.recipe_delete, name="recipe_delete"),
    path("recipe/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("recipe/<int:pk>/like/", views.toggle_like, name="toggle_like"),
    path("recipe/<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("comment/<int:pk>/edit/", views.edit_comment, name="edit_comment"),
    path("comment/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
    path("register/", views.register, name="register"),
    path("profile/<int:pk>/", views.user_profile, name="user_profile"),
    path("user/<int:pk>/follow/", views.toggle_follow, name="toggle_follow"),
    path("user/<int:pk>/followers/", views.followers_list, name="followers_list"),
    path("user/<int:pk>/following/", views.following_list, name="following_list"),
    path("feed/", views.feed, name="feed"),
    # Add more URL patterns as needed
    
  
    path('accounts/logout/', views.logout, name='logout'),
    
    
    
    # password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
