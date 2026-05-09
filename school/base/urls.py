from django.urls import path
from .import views

urlpatterns = [
       
          path('',views.home, name='home'),

          path('login/',views.LoginPage, name='loginPage'),
          path('logout/',views.Logoutpage, name='logoutPage'),
          
          path('register/',views.Register,name='registerPage'),

          path('dashboard/', views.dashboard, name='dashboard'),
          # path('add_student/', views.add_student, name='add_student'),
          
          path('features/', views.features_view, name='features'),
          
          path('about/', views.about_view, name='about'),
          path('learn-more/', views.learn_more, name='learn_more'),
          path('contact/', views.contact_view, name='contact'),
          path('pricing/', views.pricing_view, name='pricing'),
          
          # ===================== TEACHER URLS =====================
          path('teachers/', views.teacher_list, name='teacher_list'),
          path('teachers/create/', views.teacher_create, name='teacher_create'),
          path('teachers/update/<int:pk>/', views.teacher_update, name='teacher_update'),
          path('teachers/delete/<int:pk>/', views.teacher_delete, name='teacher_delete'),


          # ===================== CLASS URLS =====================
          path('classes/', views.class_list, name='class_list'),
          path('classes/create/', views.class_create, name='class_create'),
          path('classes/update/<int:pk>/', views.class_update, name='class_update'),
          path('classes/delete/<int:pk>/', views.class_delete, name='class_delete'),

          # ===================== Sections URLS =====================
          path('sections/', views.section_list, name='section_list'),
          path('sections/create/', views.section_create, name='section_create'),
          path('sections/update/<int:pk>/', views.section_update, name='section_update'),
          path('sections/delete/<int:pk>/', views.section_delete, name='section_delete'),

          # ===================== Sudents URLS =====================
]

from django.conf import settings
from django.conf.urls.static import static

# This is REQUIRED to show photos during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)