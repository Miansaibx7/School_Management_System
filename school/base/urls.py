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
          path('students/', views.student_list, name='student_list'),
          path('students/create/', views.student_create, name='student_create'),
          path('students/update/<int:pk>/', views.student_update, name='student_update'),
          path('students/delete/<int:pk>/', views.student_delete, name='student_delete'),

          # ===================== Transactions URLS =====================
          path('transactions/', views.transaction_list, name='transaction_list'),
          path('transactions/create/', views.transaction_create, name='transaction_create'),
          path('transactions/update/<int:pk>/', views.transaction_update, name='transaction_update'),
          path('transactions/delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),

          # ===================== Fees URLS ====================================
          path('fees/', views.fee_list, name='fee_list'),
          path('fees/create/', views.fee_create, name='fee_create'),
          path('fees/update/<int:pk>/', views.fee_update, name='fee_update'),
          path('fees/delete/<int:pk>/', views.fee_delete, name='fee_delete'),

          # ===================== Salary URLS ====================================
          path('salaries/', views.salary_list, name='salary_list'),
          path('salaries/create/', views.salary_create, name='salary_create'),
          path('salaries/update/<int:pk>/', views.salary_update, name='salary_update'),
          path('salaries/delete/<int:pk>/', views.salary_delete, name='salary_delete'),


          path('financial-reports/',views.financial_reports,name='financial_reports'),

]

from django.conf import settings
from django.conf.urls.static import static

# This is REQUIRED to show photos during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)