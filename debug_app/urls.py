from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.landing, name='landing'),

    # Dashboard
    path('home/', views.home, name='home'),

    # Error Management
    path('add-error/', views.add_error, name='add_error'),
    path('edit-error/<int:id>/', views.edit_error, name='edit_error'),
    path('delete-error/<int:id>/', views.delete_error, name='delete_error'),

    # Auth
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]