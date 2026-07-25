# accounts/urls.py
from django.urls import path
from . import views
 

urlpatterns = [
    # Authentication
    path('login/', views.LoginPage, name='loginPage'),
    path('logout/', views.Logoutpage, name='logoutPage'),
    path('register/', views.Register, name='registerPage'),

     # ===================== User URLS ====================================
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/update/<int:pk>/', views.user_update, name='user_update'),   # use int:pk for consistency
    path('users/delete/<int:pk>/', views.user_delete, name='user_delete'),

    # ===================== Profile URLS ====================================
    path('profile/', views.profile, name='profile'),
        
]